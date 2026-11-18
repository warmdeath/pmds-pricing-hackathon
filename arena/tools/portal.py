"""Local re-creation of the submission portal's validation (README section 1.5).

Checks, in the order the real portal describes them:

1. upload shape: one folder, or one ``.zip`` alone (stored/deflate, no
   encryption, no links/special files, no unsafe/duplicate entries, no nested
   archives, ZIP itself <= 20 MiB);
2. file rules: at most 64 files and 20 MiB of contents, allowed extensions
   only, no hidden files, name/path rules, paths <= 240 characters;
3. layout: exactly one ``agent.py``; every file inside the folder holding it;
4. every Python file is valid UTF-8 and compiles (unused helpers included);
5. a disposable copy is imported, the single concrete ``BaseAgent`` subclass is
   constructed without arguments and plays three default-scenario turns with
   the real simulator CLI: 100 ms per decision, 10 s wall clock overall,
   any exception / invalid decision / timeout rejects the upload.
"""

from __future__ import annotations

import os
import re
import resource
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[2]
VALIDATION_CONFIG = ROOT / "arena" / "configs" / "portal_validation.yaml"
BUILTIN_BUNDLES = ROOT / "src" / "dme_simulator" / "agents" / "builtin_bundles"
OPPONENTS = ROOT / "arena" / "opponents"

MAX_FILES = 64
MAX_BYTES = 20 * 1024 * 1024  # 20 MiB = 20,971,520 bytes
MAX_PATH = 240
WALL_SECONDS = 10.0
CPU_SECONDS = 20  # the real CPU allowance is not published; see ARENA.md
MODEL_EXTENSIONS = {
    ".bin", ".pt", ".pth", ".pkl", ".pickle", ".joblib", ".onnx",
    ".safetensors", ".npy", ".npz", ".h5", ".hdf5",
}
ALLOWED_EXTENSIONS = {".py"} | MODEL_EXTENSIONS
ARCHIVE_EXTENSIONS = {".zip", ".tar", ".gz", ".tgz", ".bz2", ".xz", ".7z", ".rar"}
NAME_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_. \-]*$")


class Rejected(Exception):
    """The upload is rejected; the message is the reason shown to the team."""


@dataclass
class ValidationResult:
    ok: bool
    reason: str = ""
    agent_id: str = ""
    class_name: str = ""
    files: list[str] = field(default_factory=list)
    bundle_dir: Path | None = None  # validated copy (inside a temp dir)
    wall_seconds: float = 0.0
    log: str = ""


# ---------------------------------------------------------------------------
# file rules
# ---------------------------------------------------------------------------

def _check_name(part: str, rel: str) -> None:
    if part.startswith("."):
        raise Rejected(f"hidden files or folders are not allowed: {rel}")
    if not NAME_RE.match(part):
        raise Rejected(
            f"invalid name {part!r} in {rel}: names must begin with a letter, number "
            "or underscore; the rest may also contain dots, spaces and hyphens"
        )


def _check_file_entry(rel: str) -> None:
    if len(rel) > MAX_PATH:
        raise Rejected(f"relative path longer than {MAX_PATH} characters: {rel}")
    parts = PurePosixPath(rel).parts
    for part in parts:
        _check_name(part, rel)
    suffix = PurePosixPath(rel).suffix
    if suffix.lower() in ARCHIVE_EXTENSIONS:
        raise Rejected(f"nested archives are not allowed: {rel}")
    if suffix not in ALLOWED_EXTENSIONS:
        hint = ""
        if suffix == ".pyc" or "__pycache__" in parts:
            hint = " (exclude __pycache__/ and .pyc caches from uploads)"
        raise Rejected(
            f"file extension not allowed: {rel}{hint}; allowed are .py and lowercase "
            + ", ".join(sorted(MODEL_EXTENSIONS))
        )


def _collect_folder(folder: Path) -> dict[str, Path]:
    """Return relative posix path -> file for an uploaded folder."""
    files: dict[str, Path] = {}
    for current, dirs, names in os.walk(folder, followlinks=False):
        here = Path(current)
        for name in list(dirs) + names:
            path = here / name
            rel = path.relative_to(folder).as_posix()
            mode = path.lstat().st_mode
            if stat.S_ISLNK(mode):
                raise Rejected(f"links are not allowed: {rel}")
            if name in dirs:
                _check_name(name, rel)
                continue
            if not stat.S_ISREG(mode):
                raise Rejected(f"special files are not allowed: {rel}")
            _check_file_entry(rel)
            files[rel] = path
    return files


def _extract_zip(archive: Path, target: Path) -> None:
    if archive.suffix != ".zip":
        raise Rejected("a ZIP upload must have the .zip extension")
    if archive.stat().st_size > MAX_BYTES:
        raise Rejected(f"ZIP larger than 20 MiB ({archive.stat().st_size:,} bytes)")
    try:
        bundle = zipfile.ZipFile(archive)
    except zipfile.BadZipFile as error:
        raise Rejected(f"corrupted ZIP archive: {error}") from error
    with bundle:
        seen: set[str] = set()
        total = 0
        count = 0
        for info in bundle.infolist():
            name = info.filename
            if info.flag_bits & 0x1:
                raise Rejected(f"encrypted ZIP entries are not allowed: {name}")
            if info.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                raise Rejected(f"only stored or deflate compression is allowed: {name}")
            if name.startswith("/") or "\\" in name or re.match(r"^[A-Za-z]:", name):
                raise Rejected(f"absolute or non-portable path in ZIP: {name}")
            parts = PurePosixPath(name).parts
            if ".." in parts:
                raise Rejected(f"path traversal in ZIP: {name}")
            unix_mode = info.external_attr >> 16
            if stat.S_ISLNK(unix_mode):
                raise Rejected(f"links are not allowed: {name}")
            key = name.rstrip("/")
            if key in seen:
                raise Rejected(f"duplicate ZIP entry: {name}")
            seen.add(key)
            if info.is_dir():
                for part in parts:
                    _check_name(part, name)
                continue
            if unix_mode and not (stat.S_ISREG(unix_mode) or unix_mode & 0o170000 == 0):
                raise Rejected(f"special files are not allowed: {name}")
            _check_file_entry(name)
            count += 1
            total += info.file_size
        if count > MAX_FILES:
            raise Rejected(f"too many files: {count} > {MAX_FILES}")
        if total > MAX_BYTES:
            raise Rejected(f"file contents larger than 20 MiB after extraction ({total:,} bytes)")
        bad = bundle.testzip()
        if bad is not None:
            raise Rejected(f"corrupted ZIP entry: {bad}")
        bundle.extractall(target)


# ---------------------------------------------------------------------------
# main entry point
# ---------------------------------------------------------------------------

def validate(upload: str | Path, keep_dir: Path | None = None) -> ValidationResult:
    """Validate an uploaded folder or ZIP. On success the validated bundle is
    copied to ``keep_dir/<agent_id>`` (or a temp dir) and returned."""
    upload = Path(upload)
    work = Path(tempfile.mkdtemp(prefix="arena_portal_"))
    try:
        if not upload.exists():
            raise Rejected(f"upload not found: {upload}")
        if upload.is_symlink():
            raise Rejected("links are not allowed")
        if upload.is_file():
            if upload.suffix.lower() != ".zip":
                raise Rejected("upload one folder, or one .zip file alone")
            extracted = work / "zip"
            extracted.mkdir()
            _extract_zip(upload, extracted)
            folder = extracted
        elif upload.is_dir():
            _check_name(upload.resolve().name, upload.resolve().name)
            folder = upload
        else:
            raise Rejected("special files are not allowed")

        files = _collect_folder(folder)
        if len(files) > MAX_FILES:
            raise Rejected(f"too many files: {len(files)} > {MAX_FILES}")
        total = sum(path.stat().st_size for path in files.values())
        if total > MAX_BYTES:
            raise Rejected(f"file contents larger than 20 MiB ({total:,} bytes)")

        entry_points = [rel for rel in files if PurePosixPath(rel).name == "agent.py"]
        if len(entry_points) != 1:
            raise Rejected(
                f"expected exactly one agent.py in the submission, found {len(entry_points)}"
                + (": " + ", ".join(sorted(entry_points)) if entry_points else "")
            )
        bundle_rel = PurePosixPath(entry_points[0]).parent
        if bundle_rel == PurePosixPath("."):
            bundle_src = folder
            agent_id = (upload.stem if upload.is_file() else upload.resolve().name)
            inside = list(files)
        else:
            bundle_src = folder / Path(*bundle_rel.parts)
            agent_id = bundle_rel.name
            prefix = bundle_rel.as_posix() + "/"
            outside = [rel for rel in files if not rel.startswith(prefix)]
            if outside:
                raise Rejected(
                    "all files must be inside the folder containing agent.py; outside: "
                    + ", ".join(sorted(outside)[:5])
                )
            inside = [rel[len(prefix):] for rel in files]
        _check_name(agent_id, agent_id)
        if (OPPONENTS / agent_id).exists() or (BUILTIN_BUNDLES / agent_id).exists():
            raise Rejected(
                f"team name {agent_id!r} is already taken by another team; "
                "rename your agent folder"
            )

        for rel in sorted(inside):
            if not rel.endswith(".py"):
                continue
            raw = (bundle_src / rel).read_bytes()
            try:
                source = raw.decode("utf-8")
            except UnicodeDecodeError as error:
                raise Rejected(f"{rel} is not valid UTF-8: {error}") from error
            try:
                compile(source, rel, "exec", dont_inherit=True)
            except SyntaxError as error:
                raise Rejected(
                    f"{rel} does not compile: {error.msg} (line {error.lineno})"
                ) from error

        # disposable copy
        copy_root = Path(tempfile.mkdtemp(prefix="arena_bundle_")) if keep_dir is None else keep_dir
        copy_root.mkdir(parents=True, exist_ok=True)
        bundle_dir = copy_root / agent_id
        if bundle_dir.exists():
            shutil.rmtree(bundle_dir)
        for rel in inside:
            target = bundle_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(bundle_src / rel, target)

        smoke = _smoke_test(bundle_dir, agent_id)
        return ValidationResult(
            ok=True, agent_id=agent_id, class_name=smoke[0], files=sorted(inside),
            bundle_dir=bundle_dir, wall_seconds=smoke[1], log=smoke[2],
        )
    except Rejected as rejection:
        return ValidationResult(ok=False, reason=str(rejection))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def _limit_cpu() -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_SECONDS, CPU_SECONDS + 1))


def _smoke_test(bundle_dir: Path, agent_id: str) -> tuple[str, float, str]:
    """Import, construct and play three default-scenario turns with the real CLI."""
    probe = subprocess.run(
        [sys.executable, "-c", (
            "import sys; from dme_simulator.agents.loader import load_agent_bundle_class as L;"
            "print(L(sys.argv[1]).__name__)"
        ), str(bundle_dir)],
        cwd=bundle_dir, capture_output=True, text=True, timeout=WALL_SECONDS,
        env=_env(), preexec_fn=_limit_cpu,
    )
    if probe.returncode != 0:
        raise Rejected("agent could not be loaded:\n" + _tail(probe.stderr))
    class_name = probe.stdout.strip().splitlines()[-1]

    command = [
        sys.executable, "-m", "dme_simulator",
        "--config", str(VALIDATION_CONFIG),
        "--agents-dir", str(BUILTIN_BUNDLES),
        "--extra-agent", str(bundle_dir),
        "--turns", "3", "--ui", "none",
    ]
    started = time.perf_counter()
    try:
        run = subprocess.run(
            command, cwd=bundle_dir, capture_output=True, text=True,
            timeout=WALL_SECONDS, env=_env(), preexec_fn=_limit_cpu,
        )
    except subprocess.TimeoutExpired as error:
        raise Rejected(
            f"validation exceeded the {WALL_SECONDS:.0f}-second wall-clock deadline"
        ) from error
    elapsed = time.perf_counter() - started
    log = run.stdout + run.stderr
    if run.returncode != 0:
        if run.returncode < 0 or "CPU time limit" in run.stderr:
            raise Rejected("validation exceeded the CPU allowance")
        raise Rejected("simulation failed:\n" + _tail(run.stderr))
    timeout = re.search(rf"Agent {re.escape(agent_id)} reached the decide timeout.*", run.stderr)
    if timeout:
        raise Rejected("decision timeout (100 ms): " + timeout.group(0))
    failure = re.search(
        rf"Agent {re.escape(agent_id)} failed or returned an invalid decision on turn \d+",
        run.stderr,
    )
    if failure:
        detail = run.stderr[failure.start():]
        following = detail.find("\nAgent ", 1)
        if following > 0:
            detail = detail[:following]
        raise Rejected("invalid action, wrong return type or exception:\n" + _tail(detail, 25))
    if elapsed > WALL_SECONDS:
        raise Rejected(f"validation exceeded the {WALL_SECONDS:.0f}-second wall-clock deadline")
    return class_name, elapsed, log


def _env() -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["MPLBACKEND"] = "Agg"
    return env


def _tail(text: str, lines: int = 15) -> str:
    chunk = [line for line in text.strip().splitlines() if "UV_NATIVE_TLS" not in line]
    return "\n".join("    " + line for line in chunk[-lines:])


if __name__ == "__main__":
    result = validate(sys.argv[1])
    if result.ok:
        print(f"VALID: {result.agent_id} ({result.class_name}), {len(result.files)} files, "
              f"{result.wall_seconds:.2f} s")
    else:
        print("REJECTED: " + result.reason)
        sys.exit(1)
