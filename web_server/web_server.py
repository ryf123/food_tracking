import http.server
import socketserver
import json
from db_access import DBAccess
import re
import urllib.parse
from transcribe_service import TranscribeService
# Define the port number for the server to listen on
PORT = 8000

# Create a request handler by inheriting from the SimpleHTTPRequestHandler class
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    # Override the log_message() method to suppress log messages
    def log_message(self, format, *args):
        return

    def do_POST(self):
        print(f"[do_Post]Entering path {self.path}\n")
        if self.path == "/transcribe":
            content_length = int(self.headers["Content-Length"])
            file_data = self.rfile.read(content_length)
            # Extract the file content from the file data
            file_content = re.search(rb'\r\n\r\n([\s\S]*)\r\n', file_data).group(1)
            file_name = 'tmp.webm'
            # [TODO] the file needs to be saved first, then read again before send it to whisper, not sure why
            with open(file_name, "wb") as f:
                f.write(file_content)
            ts = TranscribeService()
            text = ts.transcribe_audio_file(file_name)
            print(text)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps({'text': text}), 'utf-8'))
        elif self.path == "/calculate_calorie":
            # Get the content length from the headers
            content_length = int(self.headers['Content-Length'])

            # Read the request body
            request_body = self.rfile.read(content_length)

            # Parse the JSON data from the request body
            data = json.loads(request_body)
            # Process the data as needed
            ts = TranscribeService()
            print(data)
            calories = ts.summarize_calorie_intake(data['transcribed_text'])
            print(calories)
            # Send the response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(bytes(json.dumps(calories), 'utf-8'))
        else:
            super.do_POST()

    # Override the do_GET() method to customize the homepage
    def do_GET(self):
        print(f"[do_GET]Entering path {self.path}\n")
        parsed_url = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_url.query)

        if self.path == "/":
            # Customize the content for the homepage
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('homepage.html', 'r') as f:
                self.wfile.write(bytes(f.read(), encoding='utf-8'))

        elif self.path == "/dashboard":
            # Customize the content for the homepage
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('dashboard.html', 'r') as f:
                self.wfile.write(bytes(f.read(), encoding='utf-8'))

        elif self.path.startswith("/db_save"):
            print(query_params.get('text', [''])[0])

            db_access = DBAccess()
            db_access.insert_to_db(200, json.loads(query_params.get('text', [''])[0]))
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')  # Add the Content-type header
            self.end_headers()

        elif self.path.startswith("/load_history"):
            self.send_response(200)
            user_id = query_params.get('user_id', [''])[0]
            print(f'user id: {user_id}')
            db_access = DBAccess()
            calorie_data = db_access.get_calorie(user_id)
            self.send_header('Content-type', 'application/text')  # Add the Content-type header
            self.end_headers()
            print(calorie_data)
            self.wfile.write(bytes(json.dumps(calorie_data), 'utf-8'))
            
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