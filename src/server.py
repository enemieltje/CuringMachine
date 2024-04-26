from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import io
import logging
import socketserver
import multiprocessing
from http import server
from camera import output, Camera


PAGE = """\
<html>
<head>
<title>Curing Machine</title>
</head>
<body>
<h1>Pi Camera Live Stream Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
<a href="button/startcam">Start Preview</a>
<a href="button/stopcam">Stop Preview</a>
</body>
</html>
"""


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer, multiprocessing.Process):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self):
        super(multiprocessing.Process, self).__init__()

    def run(self):
        try:
            # Set up and start the streaming server
            self.serve_forever()
        finally:
            # Stop recording when the script is interrupted
            print("Stream stopped.")


class Server():
    port = 8080
    cameras = list()
    webServer: StreamingServer

    def startStreamServer():
        address = ('', 8000)
        # self.cameras[0].startStream()
        streamServer = StreamingServer(address, StreamingHandler)
        streamServer.start()

    def addCamera(camera: Camera):
        Server.cameras.append(camera)


# Class to handle HTTP requests
class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirect root path to index.html
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Serve the HTML page
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            # Set up MJPEG streaming
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header(
                'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        elif self.path == '/button/startcam':
            Server.cameras[0].startStream()
        elif self.path == '/button/stopcam':
            Server.cameras[0].stopStream()
        else:
            # Handle 404 Not Found
            self.send_error(404)
            self.end_headers()
