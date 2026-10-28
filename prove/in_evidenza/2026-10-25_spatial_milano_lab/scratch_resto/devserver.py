"""Server statico locale + POST /save?name=x.png per salvare screenshot del canvas (solo per i test)."""
import http.server, os, urllib.parse

os.makedirs("shots", exist_ok=True)


class H(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        q = urllib.parse.urlparse(self.path)
        name = os.path.basename(urllib.parse.parse_qs(q.query).get("name", ["x.png"])[0])
        data = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        open(os.path.join("shots", name), "wb").write(data)
        self.send_response(200); self.end_headers(); self.wfile.write(b"ok")


http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
