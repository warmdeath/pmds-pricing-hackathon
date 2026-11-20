"""Serve the browser version locally and share progress with the terminal trainer.

    course/run.sh web          (builds, then runs this on http://localhost:8765)

GET  /api/progress  -> the contents of course/.progress.json
PUT  /api/progress  -> merge the body into that file (same rules as the terminal),
                       write it, and return the merged result

The terminal trainer reads and writes the same file, so the two stay in step.
Listens on 127.0.0.1 only.
"""

from __future__ import annotations

import json
import os
import sys
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.dont_write_bytecode = True
WEB = Path(__file__).resolve().parent
sys.path.insert(0, str(WEB.parent))

import progress  # noqa: E402

LOCK = threading.Lock()
MAX_BODY = 5 * 1024 * 1024


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):  # keep the terminal quiet
        pass

    def _json(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/progress":
            with LOCK:
                return self._json(200, progress.read_file(progress.STATE_FILE))
        return super().do_GET()

    def do_PUT(self):
        if self.path.split("?")[0] != "/api/progress":
            return self._json(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > MAX_BODY:
            return self._json(400, {"error": "bad length"})
        try:
            incoming = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            return self._json(400, {"error": "invalid JSON"})
        with LOCK:
            merged = progress.merge(progress.read_file(progress.STATE_FILE), incoming)
            progress.write_file(merged, progress.STATE_FILE)
        return self._json(200, merged)


def main() -> None:
    port = int(os.environ.get("COURSE_WEB_PORT", "8765"))
    handler = partial(Handler, directory=str(WEB / "dist"))
    server = ThreadingHTTPServer(("127.0.0.1", port), handler)
    print(f"Margin Notes is running at http://localhost:{port}  (Ctrl+C to stop)")
    print(f"progress is shared with the terminal through {progress.STATE_FILE}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
