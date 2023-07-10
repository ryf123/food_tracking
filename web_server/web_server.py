import http.server
import socketserver

# Define the port number for the server to listen on
PORT = 8000

# Create a request handler by inheriting from the SimpleHTTPRequestHandler class
class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    # Override the log_message() method to suppress log messages
    def log_message(self, format, *args):
        return

    # Override the do_GET() method to customize the homepage
    def do_GET(self):
        if self.path == "/":
            # Customize the content for the homepage
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open('homepage.html', 'r') as f:
                self.wfile.write(bytes(f.read(), encoding='utf-8'))
        else:
            # Serve other files as usual
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