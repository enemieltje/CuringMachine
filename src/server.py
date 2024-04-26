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


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True
    process: multiprocessing.Process

    def __init__(self, address, streamingHandler):
        super().__init__(address, streamingHandler)

    def run(self):
        try:
            # Set up and start the streaming server
            self.serve_forever()
        finally:
            # Stop recording when the script is interrupted
            print("Stream stopped.")

    def start(self):
        self.run()
        # self.process = multiprocessing.Process(target=self.run)
        # self.process.start()

    def stop(self):
        self.shutdown()
        self.process.terminate()
        self.process.kill()


class Server():
    port = 8080
    cameras = list()
    streamServer: StreamingServer

    def start():
        address = ('', Server.port)
        # self.cameras[0].startStream()
        Server.streamServer = StreamingServer(address, StreamingHandler)
        Server.streamServer.start()

    def stop():
        Server.streamServer.stop()
        Server.streamServer.server_close()
        for camera in Server.cameras:
            camera.stopStream()

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
            print("start cam")
            for camera in Server.cameras:
                camera.startStream()
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/button/stopcam':
            print("stop cam")
            for camera in Server.cameras:
                camera.stopStream()
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        else:
            # Handle 404 Not Found
            self.send_error(404)
            self.end_headers()
