import logging
import os
import socketserver
import multiprocessing
from http import server
from camera import Camera
from belt import Belt

logger = logging.getLogger(__name__)


class Server(socketserver.ThreadingMixIn, server.HTTPServer):
    port = 8080
    cameras = list()
    instance: any
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

    def start():
        address = ('', Server.port)
        Server.instance = Server(address, StreamingHandler)
        Server.instance.run()

        logger.info('Server running at',
                    Server.instance.server_address)

    def stop():
        Server.instance.shutdown()
        Server.instance.server_close()
        for camera in Server.cameras:
            camera.stopStream()

    def addCamera(camera: Camera):
        Server.cameras.append(camera)

# Class to handle HTTP requests


class StreamingHandler(server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirect root path to index.html
            self.redirectHome(permanently=True)

        elif self.path == '/favicon.ico':
            self.sendFile('src/client/favicon.ico')

        elif self.path == '/index.html':
            self.sendFile('src/client/index.html')

        elif self.path == '/index.js':
            self.sendFile('src/client/index.js')

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
            while Server.cameras[0].isStreaming:
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

    def redirectHome(self, permanently=False):
        if permanently:
            self.send_response(301)
        else:
            self.send_response(302)
        self.send_header('Location', '/index.html')
        self.end_headers()

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

    def sendFile(self, filePath):
        logger.debug("sending file: " + filePath)
        if not os.path.isfile(filePath):
            logger.warn('File does not exist: ' + filePath)
            self.redirectHome()
            return
        self.path = filePath
        server.SimpleHTTPRequestHandler.do_GET(self)
