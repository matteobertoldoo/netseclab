from http.server import BaseHTTPRequestHandler, HTTPServer

class FakeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"I have been hacked")

if __name__ == "__main__":
    server = HTTPServer(("", 80), FakeHandler)
    server.serve_forever()
