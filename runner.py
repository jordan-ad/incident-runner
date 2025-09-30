import json
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

SLACK_WEBHOOK = "https://hooks.slack.com/triggers/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"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_len)
        payload = body.decode("utf-8")

        # Run the curl command
        curl_cmd = [
            "curl", "-X", "POST", SLACK_WEBHOOK,
            "-H", "Content-Type: application/json",
            "-d", payload
        ]
        result = subprocess.run(curl_cmd, capture_output=True, text=True)

        # Respond
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            "ok": True,
            "sent": json.loads(payload),
            "curl_stdout": result.stdout,
            "curl_stderr": result.stderr
        }).encode())

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 5000), Handler)
    print("Listening on http://0.0.0.0:5000")
    server.serve_forever()
