import os
import http.server
import socketserver
import urllib.parse

class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        base = os.path.dirname(os.path.abspath(__file__))
        parsed = urllib.parse.urlparse(path)
        route = parsed.path.strip('/').split('/')[0]
        if route in ('naukri', 'naukri-redesign', 'tender', 'mandi', 'cutoff', 'startup'):
            return os.path.join(base, route, 'index.html')
        if route == '' or route == 'index.html':
            return os.path.join(base, 'index.html')
        return os.path.join(base, parsed.path.lstrip('/'))

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    with socketserver.TCPServer(('', port), Handler) as httpd:
        print(f'Serving multi-module fixture on http://127.0.0.1:{port}')
        httpd.serve_forever()
