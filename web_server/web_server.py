import http.server
import socketserver
import json
from db_access import DBAccess
from transcribe_service import TranscribeService
# Define the port number for the server to listen on
PORT = 8000

# Create a request handler by inheriting from the SimpleHTTPRequestHandler class
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    # Override the log_message() method to suppress log messages
    def log_message(self, format, *args):
        return

    # Override the do_GET() method to customize the homepage
    def do_GET(self):
        print(f"[do_GET]Entering path {self.path}\n")

        if self.path == "/":
            # Customize the content for the homepage
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('homepage.html', 'r') as f:
                self.wfile.write(bytes(f.read(), encoding='utf-8'))
        elif self.path == "/transcribe":
            self.send_response(200)
            ts = TranscribeService()
            text = ts.transcribe_audio()
            print(text)
            calories = ts.summarize_calorie_intake(text)
            print(calories)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(calories), 'utf-8'))

        elif self.path.startswith("/db_save"):
            import urllib.parse
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            print(query_params.get('text', [''])[0])

            db_access = DBAccess()
            db_access.insert_to_db(200, query_params.get('text', [''])[0])
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')  # Add the Content-type header
            self.end_headers()

        else:
            super().do_GET()

# Create an instance of the HTTP server with the defined port and request handler
with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
    print(f"Server running on port {PORT}")
    # Start the server and keep it running until interrupted
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer interrupted. Stopping...")
        httpd.server_close()