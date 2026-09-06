import http.server
import socketserver
import os
import webbrowser
import json

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIRECTORY)


class FamilyTreeHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/save":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                data = json.loads(body)
                with open("family_tree_base.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                response = json.dumps({"status": "ok"}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response)
            except Exception as e:
                response = json.dumps({"status": "error", "message": str(e)}).encode("utf-8")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(response)
        else:
            response = json.dumps({"status": "error", "message": "Not found"}).encode("utf-8")
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def end_headers(self):
        if "Access-Control-Allow-Origin" not in str(self._headers_buffer):
            self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()


socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), FamilyTreeHandler) as httpd:
    url = f"http://localhost:{PORT}"
    print(f"Serving family tree at {url}")
    print(f"  Tree view:  {url}/family_tree_structure.html")
    print(f"  List view:  {url}/html_family_tree_in_list.html")
    print(f"\nPress Ctrl+C to stop the server.")
    webbrowser.open(f"{url}/family_tree_structure.html")
    httpd.serve_forever()
