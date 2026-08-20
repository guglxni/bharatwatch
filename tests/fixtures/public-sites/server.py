from http.server import HTTPServer, SimpleHTTPRequestHandler
import os, sys

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        base = os.path.dirname(os.path.abspath(__file__))
        route = path.strip('/').split('/')[0] if path.strip('/') else ''
        if route in ('naukri', 'naukri-redesign', 'tender', 'mandi', 'cutoff', 'startup'):
            return os.path.join(base, route, 'index.html')
        return os.path.join(base, 'index.html')

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
    httpd = HTTPServer(('127.0.0.1', port), Handler)
    print(f'Serving multi-module fixture on http://127.0.0.1:{port}')
    httpd.serve_forever()
