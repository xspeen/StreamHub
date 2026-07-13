#!/usr/bin/env python3
"""
StreamHub HTTP Server
Lightweight Python server that serves the web UI and API endpoints.
Uses only Python standard library - no external packages.

Endpoints:
  GET  /                  - Serves index.html
  GET  /api/profile       - Returns user profile as JSON
  POST /api/profile       - Saves user profile from JSON body
  POST /api/auth          - Validates passcode or changes passcode
  GET  /api/channels      - Returns channels for a category
  GET  /api/categories    - Returns category list
"""

import json
import os
import sys
import signal
import hashlib
import datetime
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class StreamHubHandler(BaseHTTPRequestHandler):
    """HTTP request handler for StreamHub server."""

    # Class-level config (set before server starts)
    data_dir = ""
    web_dir = ""
    db = None
    live_ips = {}  # ip -> last_seen timestamp

    def log_message(self, format, *args):
        """Suppress default request logging for cleaner terminal output."""
        pass

    def send_cors_headers(self):
        """Add CORS headers for local development."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def send_json(self, data, status=200):
        """Send a JSON response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, filepath, content_type="text/html"):
        """Send a file response."""
        try:
            with open(filepath, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_cors_headers()
            if content_type.startswith("text/html"):
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
                self.send_header("Pragma", "no-cache")
                self.send_header("Expires", "0")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error_page(404, "Not Found")

    def send_error_page(self, code, message):
        """Send a simple error response."""
        body = json.dumps({"error": message}).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_cors_headers()
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self):
        """Read the request body as a string."""
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return ""
        return self.rfile.read(length).decode("utf-8", errors="replace")

    def get_client_ip(self):
        """Get the client's IP address from the request."""
        # Check X-Forwarded-For first (for proxied requests)
        xff = self.headers.get("X-Forwarded-For", "")
        if xff:
            return xff.split(",")[0].strip()
        # Fall back to connection address
        addr = self.client_address
        if addr:
            return addr[0]
        return "127.0.0.1"

    def check_device_access(self):
        """Check if the client IP is allowed. Returns True if allowed."""
        ip = self.get_client_ip()
        if ip in ("127.0.0.1", "::1", "localhost"):
            return True
        # Track live IPs
        self.__class__.live_ips[ip] = datetime.datetime.now().timestamp()
        return self.db.is_device_allowed(ip)

    def handle_get(self, path, query):
        """Handle GET requests."""
        # Root - serve index.html
        if path == "/" or path == "":
            index_path = os.path.join(self.web_dir, "index.html")
            self.send_file(index_path, "text/html; charset=utf-8")
            return

        # Static files from web directory
        if path.startswith("/web/"):
            rel_path = path[5:]
            file_path = os.path.join(self.web_dir, rel_path)
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                ct = {
                    ".html": "text/html; charset=utf-8",
                    ".css": "text/css",
                    ".js": "application/javascript",
                    ".json": "application/json",
                    ".png": "image/png",
                    ".jpg": "image/jpeg",
                    ".svg": "image/svg+xml",
                    ".ico": "image/x-icon",
                }.get(ext, "application/octet-stream")
                self.send_file(file_path, ct)
            else:
                self.send_error_page(404, "Not Found")
            return

        # API: Get profile
        if path == "/api/profile":
            profile = self.db.get_profile()
            self.send_json(profile)
            return

        # API: Get my IP (for the client to know its own IP)
        if path == "/api/myip":
            self.send_json({"ip": self.get_client_ip()})
            return

        # API: Get current version
        if path == "/api/version":
            ver_path = os.path.join(os.path.dirname(self.data_dir), "VERSION")
            try:
                with open(ver_path, "r") as f:
                    ver = f.read().strip()
            except IOError:
                ver = "unknown"
            self.send_json({"version": ver})
            return

        # API: Get allowed devices (admin only)
        if path == "/api/devices":
            devices = self.db.get_allowed_devices()
            # Clean up stale live IPs (older than 30 seconds)
            now = datetime.datetime.now().timestamp()
            stale = [ip for ip, ts in self.__class__.live_ips.items() if now - ts > 30]
            for ip in stale:
                del self.__class__.live_ips[ip]
            # Also track admin's own IP as live
            admin_ip = self.get_client_ip()
            if admin_ip not in ("127.0.0.1", "::1", "localhost"):
                self.__class__.live_ips[admin_ip] = now
            self.send_json({"devices": devices, "live_ips": list(self.__class__.live_ips.keys())})
            return

        # API: Get categories (requires device access)
        if path == "/api/categories":
            if not self.check_device_access():
                self.send_json({"error": "Access denied"}, 403)
                return
            from scanner import build_categories
            cats = build_categories()
            simple_cats = []
            for c in cats:
                simple_cats.append({
                    "id": c["id"],
                    "name": c["name"],
                    "icon": c["icon"],
                    "type": c["type"]
                })
            self.send_json(simple_cats)
            return

        # API: Get channels (requires device access)
        if path == "/api/channels":
            if not self.check_device_access():
                self.send_json({"error": "Access denied"}, 403)
                return
            cat_id = query.get("category", [""])[0]
            if not cat_id:
                self.send_json({"error": "category parameter required"}, 400)
                return

            from scanner import build_categories, fetch_category_channels

            cats = build_categories()
            cat = None
            for c in cats:
                if c["id"] == cat_id:
                    cat = c
                    break

            if not cat:
                self.send_json({"error": "Unknown category"}, 404)
                return

            cached = self.db.get_cached_channels()
            if cached and cat_id in cached:
                self.send_json(cached[cat_id])
                return

            channels = fetch_category_channels(cat)

            cache = self.db.get_cached_channels() or {}
            cache[cat_id] = channels
            self.db.save_channel_cache(cache)

            self.send_json(channels)
            return

        self.send_error_page(404, "Not Found")

    def handle_post(self, path, query):
        """Handle POST requests."""
        body = self.read_body()

        # API: Save profile
        if path == "/api/profile":
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self.send_json({"error": "Invalid JSON"}, 400)
                return

            profile = self.db.get_profile()
            if "name" in data:
                profile["name"] = str(data["name"])[:50]
            if "avatar" in data:
                profile["avatar"] = str(data["avatar"])[:5]
            if "photo" in data:
                photo = str(data["photo"])
                if len(photo) > 600000:
                    photo = photo[:600000]
                profile["photo"] = photo
            elif "photo" in data and not data["photo"]:
                profile["photo"] = ""
            profile["last_login"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

            self.db.save_profile(profile)
            self.send_json({"status": "ok", "profile": profile})
            return

        # API: Manage devices (add/remove/toggle)
        if path == "/api/devices":
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self.send_json({"error": "Invalid JSON"}, 400)
                return

            action = data.get("action", "")

            if action == "add":
                ip = data.get("ip", "").strip()
                name = data.get("name", "").strip()
                ok, msg = self.db.add_device(ip, name)
                self.send_json({"status": "ok" if ok else "error", "message": msg})
                return

            elif action == "remove":
                ip = data.get("ip", "").strip()
                self.db.remove_device(ip)
                self.send_json({"status": "ok"})
                return

            elif action == "toggle":
                ip = data.get("ip", "").strip()
                new_state = self.db.toggle_device(ip)
                if new_state is not None:
                    self.send_json({"status": "ok", "enabled": new_state})
                else:
                    self.send_json({"status": "error", "message": "Device not found"}, 404)
                return

            self.send_json({"error": "Unknown action"}, 400)
            return

        # API: Auth (verify or change passcode)
        if path == "/api/auth":
            try:
                data = json.loads(body) if body else {}
            except json.JSONDecodeError:
                self.send_json({"error": "Invalid JSON"}, 400)
                return

            action = data.get("action", "verify")

            if action == "verify":
                passcode = data.get("passcode", "")
                if self.db.verify_passcode(passcode):
                    self.send_json({"status": "ok", "authenticated": True})
                else:
                    self.send_json({"status": "error", "authenticated": False, "message": "Incorrect passcode"}, 401)
                return

            elif action == "change_passcode":
                current = data.get("current_passcode", "")
                new_pass = data.get("new_passcode", "")

                if not self.db.verify_passcode(current):
                    self.send_json({"status": "error", "message": "Current passcode is incorrect"}, 401)
                    return

                if len(new_pass) < 1:
                    self.send_json({"status": "error", "message": "New passcode cannot be empty"}, 400)
                    return

                self.db.set_passcode(new_pass)
                self.send_json({"status": "ok"})
                return

            elif action == "set_passcode":
                # First-run: set passcode without requiring current
                passcode = data.get("passcode", "")
                if len(passcode) < 1:
                    self.send_json({"status": "error", "message": "Passcode cannot be empty"}, 400)
                    return
                self.db.set_passcode(passcode)
                self.send_json({"status": "ok"})
                return

            elif action == "reset_passcode":
                # Reset passcode after failed attempts (forgot passcode)
                new_pass = data.get("new_passcode", "")
                if len(new_pass) < 1:
                    self.send_json({"status": "error", "message": "Passcode cannot be empty"}, 400)
                    return
                self.db.set_passcode(new_pass)
                self.send_json({"status": "ok", "authenticated": True})
                return

            self.send_json({"error": "Unknown action"}, 400)
            return

        self.send_error_page(404, "Not Found")

    def do_GET(self):
        """Route GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        self.handle_get(path, query)

    def do_POST(self):
        """Route POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        self.handle_post(path, query)

    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_cors_headers()
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()


def find_python():
    """Find a suitable Python interpreter."""
    for cmd in ["python3", "python"]:
        try:
            import subprocess
            result = subprocess.run(
                [cmd, "--version"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                ver = result.stdout.strip()
                parts = ver.replace("Python ", "").split(".")
                if len(parts) >= 2:
                    major, minor = int(parts[0]), int(parts[1])
                    if major >= 3 and minor >= 7:
                        return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    return None


def main():
    """Start the StreamHub server."""
    parser = argparse.ArgumentParser(description="StreamHub Server")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on")
    parser.add_argument("--data", type=str, default="", help="Data directory path")
    parser.add_argument("--web", type=str, default="", help="Web directory path")
    args = parser.parse_args()

    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(script_dir)

    data_dir = args.data or os.path.join(base_dir, "data")
    web_dir = args.web or os.path.join(base_dir, "web")

    # Initialize database
    from db import StreamHubDB
    db = StreamHubDB(data_dir)

    # Set class-level config
    StreamHubHandler.data_dir = data_dir
    StreamHubHandler.web_dir = web_dir
    StreamHubHandler.db = db

    # Handle SIGINT for clean shutdown (works in Termux)
    def signal_handler(sig, frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start server
    port = args.port
    max_retries = 10

    for attempt in range(max_retries):
        try:
            server = HTTPServer(("0.0.0.0", port), StreamHubHandler)
            server.serve_forever()
        except OSError as e:
            if "Address already in use" in str(e) or "errno 98" in str(e).lower():
                port += 1
                if attempt < max_retries - 1:
                    continue
            sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == "__main__":
    main()
