from http.server import SimpleHTTPRequestHandler
from http.server import HTTPServer
import subprocess
import json
import datetime

class MyHandler(SimpleHTTPRequestHandler):
   def do_GET(self):
    if self.path == '/get_data':
        # Run your MTAdata.py script to generate the latest JSON
        subprocess.run(['python', 'MTAdata.py'])
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # Allow requests from any origin
        self.end_headers()
        with open('stopsGraph.json', 'rb') as file:  # Open the file in binary mode
            self.copyfile(file, self.wfile)
    else:
        # Serve other files as usual
        super().do_GET()



if __name__ == "__main__":
    PORT = 8000
    httpd = HTTPServer(('localhost', PORT), MyHandler)
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
