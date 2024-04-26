from _socket import _RetAddress
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import BaseServer
import time


class Server():
    hostName = "localhost"
    port: int
    webServer: HTTPServer

    def __init__(self, port=8080):
        self.port = port
        self.webServer = HTTPServer((self.hostName, self.port), RequestHandler)
        print("Server started http://%s:%s" % (self.hostName, self.port))

        try:
            self.webServer.serve_forever()
        except KeyboardInterrupt:
            pass

        self.webServer.server_close()
        print("Server stopped.")


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(
            bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))
        self.wfile.write(
            bytes("<p>This is an example web server.</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
