import logging
import os
import socketserver
from http import server
from config import Config
from curingMachine import CuringMachine

logger = logging.getLogger(__name__)


class Server(socketserver.ThreadingMixIn, server.HTTPServer):
    # A simple HTTP server allowing IO over a webpage

    port = Config.getWebPort()
    instance: any
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, address, requestHandler):
        super().__init__(address, requestHandler)

    def run(self):
        logger.info('Server running at' +
                    str(Server.instance.server_address))
        try:
            # Set up and start the server
            self.serve_forever()
        finally:
            # Stop serving when the script is interrupted
            logger.info("Stream stopped.")

    def start():
        # This creates an instance of the server class and runs it
        logger.debug('starting server...')
        logger.debug('sever port %i', Server.port)
        address = ('', Server.port)
        Server.instance = Server(address, RequestHandler)
        Server.instance.run()

    def stop():
        # This shuts the instance down and stops all camera streams
        logger.debug('stopping server')
        Server.instance.shutdown()
        Server.instance.server_close()


class RequestHandler(server.SimpleHTTPRequestHandler):
    # This handles the requests sent to the http server (from the fetch function in index.js for example)
    # Requests always contain a path/url that describes what the request wants from the server

    def do_GET(self):
        # read the request url and call the appropriate function
        if self.path == '/':
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
            CuringMachine.startCam()
            self.redirectHome()

        elif self.path == '/button/stopcam':
            CuringMachine.stopCam()
            self.redirectHome()

        elif self.path == '/button/picture':
            self.sendStream('image/png', CuringMachine.picture())

        elif self.path == '/button/showcase':
            CuringMachine.showcase()
            self.redirectHome()

        else:
            # An unknown request was sent
            server.SimpleHTTPRequestHandler.do_GET(self)

    def stream(self):
        # Set up MJPEG streaming from the streamingOutput from the first camera
        self.send_response(200)
        self.send_header('Age', 0)
        self.send_header('Cache-Control', 'no-cache, private')
        self.send_header('Pragma', 'no-cache')
        self.send_header(
            'Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
        self.end_headers()
        # TODO: Add multi camera support
        output = CuringMachine.cameras[0].streamingOutput
        try:
            while CuringMachine.cameras[0].isStreaming:
                # Send frames from the buffer while the camera is streaming
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
            # If the stream stopped or crashed, send a warning
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

    def sendPageNotFound(self):
        self.send_error(404)
        self.end_headers()

    def sendStream(self, contentType, content):
        # This sends a file in the form of a byte stream to the webpage
        self.send_response(200)
        self.send_header('Content-Type', contentType)
        self.send_header('Content-Length', len(content))
        self.end_headers()
        self.wfile.write(content)

    def sendFile(self, filePath):
        # This opens a file on the raspberry and sends that to the webpage
        logger.debug("sending file: " + filePath)
        if not os.path.isfile(filePath):
            # If the file does not exist, send a warning and redirect to the home page
            logger.warn('File does not exist: ' + filePath)
            self.redirectHome()
            return

        # The built-in class "SimpleHTTPRequestHandler", which this class extends, already has this functionality
        # This wrapper allows us to have the request path and the file path not be the same, and handle non-existent files correctly as above
        self.path = filePath
        server.SimpleHTTPRequestHandler.do_GET(self)
