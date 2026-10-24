#!/usr/bin/env python3
"""
============================================================
 MD Mostafizur Rahman - Portfolio Local Server
============================================================
A lightweight, zero-dependency HTTP server to host and test
the portfolio website locally. Also handles contact form
submissions and stores messages in 'messages.json'.

Usage:
    python server.py
    python server.py --port 8080
    python server.py --no-browser
============================================================
"""

import http.server
import socketserver
import os
import sys
import json
import urllib.parse
import webbrowser
from datetime import datetime

# Server Configuration
DEFAULT_PORT = 3000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MESSAGES_FILE = os.path.join(DIRECTORY, "messages.json")


class PortfolioRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler for serving portfolio assets and handling APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_POST(self):
        """Handle contact form submissions at /api/contact."""
        if self.path == "/api/contact":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8")
                
                # Try parsing as JSON or URL-encoded form data
                try:
                    payload = json.loads(post_data)
                except Exception:
                    parsed = urllib.parse.parse_qs(post_data)
                    payload = {k: v[0] for k, v in parsed.items()}

                # Extract fields
                name = payload.get("name") or payload.get("userName", "Anonymous")
                email = payload.get("email") or payload.get("userEmail", "N/A")
                subject = payload.get("subject") or payload.get("userSubject", "No Subject")
                message = payload.get("message") or payload.get("userMessage", "")

                new_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "name": name,
                    "email": email,
                    "subject": subject,
                    "message": message,
                    "client_ip": self.client_address[0]
                }

                # Save message to messages.json
                existing_messages = []
                if os.path.exists(MESSAGES_FILE):
                    try:
                        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
                            existing_messages = json.load(f)
                    except Exception:
                        existing_messages = []

                existing_messages.append(new_entry)

                with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
                    json.dump(existing_messages, f, indent=4, ensure_ascii=False)

                print(f"[Contact Received] From: {name} ({email}) | Subject: {subject}")

                # Send JSON success response
                response = {
                    "status": "success",
                    "message": f"Thank you {name}, your message has been received!"
                }
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
                return

            except Exception as e:
                print(f"[Error] Failed to process contact submission: {e}")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
                return

        # Default fallback for unknown POST
        self.send_response(404)
        self.end_headers()

    def end_headers(self):
        """Add modern security and caching headers."""
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def log_message(self, format, *args):
        """Clean terminal logging."""
        sys.stdout.write(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]} -> {args[1]}\n")


def get_available_port(start_port):
    """Find an open port starting from start_port."""
    import socket
    port = start_port
    while port < start_port + 50:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", port)) != 0:
                return port
            port += 1
    return start_port


def run():
    # Parse CLI arguments
    port = DEFAULT_PORT
    auto_open_browser = True

    for arg in sys.argv[1:]:
        if arg.startswith("--port="):
            port = int(arg.split("=")[1])
        elif arg == "--no-browser":
            auto_open_browser = False

    # Check if specified port is free, or find next available
    server_port = get_available_port(port)
    server_url = f"http://localhost:{server_port}"

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", server_port), PortfolioRequestHandler) as httpd:
        print("\n" + "=" * 60)
        print("  MD MOSTAFIZUR RAHMAN - PORTFOLIO LOCAL SERVER")
        print("=" * 60)
        print(f"  > Server Directory : {DIRECTORY}")
        print(f"  > Local URL        : {server_url}")
        print(f"  > Contact API      : {server_url}/api/contact")
        print(f"  > Messages Log     : {MESSAGES_FILE}")
        print("=" * 60)
        print("  [Tip] Press Ctrl + C to stop the server at any time.\n")

        if auto_open_browser and "--no-browser" not in sys.argv:
            try:
                webbrowser.open(server_url)
            except Exception:
                pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Server Stopped] Shutting down gracefully. Goodbye!")
            httpd.server_close()


if __name__ == "__main__":
    run()
