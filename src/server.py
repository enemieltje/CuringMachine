import logging
import os
import socketserver
import multiprocessing
from http import server
from camera import Camera
from belt import Belt

logger = logging.getLogger(__name__)

PAGE = """\
<!DOCTYPE html>
<html>
<head>
<title>Curing Machine</title>
</head>
<body>
<h1>Pi Camera Live Stream Demo</h1>
<img src="stream.mjpg" width="640" height="480" />
<br>
<a href="button/startcam">Start Preview</a>
<a href="button/stopcam">Stop Preview</a>
<br>
<a href="button/showcase">Showcase Motors</a>
<br>
<a href="button/picture">Take Picture</a>
</body>
</html>
"""


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address, streamingHandler):
        super().__init__(address, streamingHandler)

    def run(self):
        try:
            # Set up and start the streaming server
            self.serve_forever()
        finally:
            # Stop recording when the script is interrupted
            logger.info("Stream stopped.")


class Server():
    port = 8080
    cameras = list()
    streamServer: StreamingServer

    def start():
        address = ('', Server.port)
        Server.streamServer = StreamingServer(address, StreamingHandler)
        Server.streamServer.run()

        logger.info('Server running at', Server.streamServer.server_address)

    def stop():
        Server.streamServer.shutdown()
        Server.streamServer.server_close()
        for camera in Server.cameras:
            camera.stopStream()

    def addCamera(camera: Camera):
        Server.cameras.append(camera)


# Class to handle HTTP requests
class StreamingHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirect root path to index.html
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()

        elif self.path == '/favicon.ico':
            self.favicon()

        elif self.path == '/index.html':
            self.homePage()

        elif self.path == '/stream.mjpg':
            self.stream()

        elif self.path == '/button/startcam':
            self.startCam()

        elif self.path == '/button/stopcam':
            self.stopCam()

        elif self.path == '/button/picture':
            self.picture()

        elif self.path == '/button/showcase':
            self.showcase()

        else:
            # Handle 404 Not Found
            logger.warn("Request for unknown path:", self.path)
            self.sendPageNotFound()

    def stream(self):
        # Set up MJPEG streaming
        self.send_response(200)
        self.send_header('Age', 0)
        self.send_header('Cache-Control', 'no-cache, private')
        self.send_header('Pragma', 'no-cache')
        self.send_header(
            'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
        self.end_headers()
        output = Server.cameras[0].streamingOutput
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

    def homePage(self):
        # Serve the HTML page
        content = PAGE.encode('utf-8')
        self.sendStream('text/html', content)

    def redirectHome(self):
        self.send_response(302)
        self.send_header('Location', '/index.html')
        self.end_headers()

    def favicon(self):
        self.path = 'src/client/favicon.ico'
        server.SimpleHTTPRequestHandler.do_GET(self)

    def showcase(self):
        logger.debug("showcase")
        process = multiprocessing.Process(target=Belt.showcase)
        process.start()
        self.redirectHome()

    def startCam(self):
        logger.debug("start cam")
        for camera in Server.cameras:
            camera.startStream()
        self.redirectHome()

    def stopCam(self):
        logger.debug("stop cam")
        for camera in Server.cameras:
            camera.stopStream()
        self.redirectHome()

    def picture(self):
        logger.debug("picture")
        imageStream = Server.cameras[0].picture()
        self.sendStream('image/png', imageStream)

    def sendPageNotFound(self):
        self.send_error(404)
        self.end_headers()

    def sendStream(self, contentType, content):
        self.send_response(200)
        self.send_header('Content-Type', contentType)
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)

    def sendFile(self, contentType, filePath):
        logger.debug("sending file: " + filePath)
        if not os.path.isfile(filePath):
            logger.warn('File does not exist: ' + filePath)
            self.redirectHome()
            return
        f = open(filePath, encoding='utf-8')
        self.sendStream(contentType, f.read())
