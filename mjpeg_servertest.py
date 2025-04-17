#!/usr/bin/python3

import io
import logging
import socketserver
import asyncio
from http import server
from threading import Condition, Thread

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import gamepad_test  # Import the joystick values

PAGE = """\
<html>
<head>
<title>Picamera2 MJPEG Streaming + Joystick</title>
<meta http-equiv="refresh" content="1">
</head>
<body>
<h1>Camera Feed + Joystick Readout</h1>
<img src="stream.mjpg" width="640" height="480" /><br><br>
<h2>Joystick Values:</h2>
<p>Left Stick: X = {left_X}, Y = {left_Y}</p>
<p>Right Stick: X = {right_X}, Y = {right_Y}</p>
</body>
</html>
"""

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Inject current joystick values into the page
            content = PAGE.format(
                left_X=gamepad_test.latest_values["left_X"],
                left_Y=gamepad_test.latest_values["left_Y"],
                right_X=gamepad_test.latest_values["right_X"],
                right_Y=gamepad_test.latest_values["right_Y"]
            ).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
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
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Start joystick reader in its own thread
def start_joystick_reader():
    asyncio.run(gamepad_test.read_joystick_values())

joystick_thread = Thread(target=start_joystick_reader, daemon=True)
joystick_thread.start()

# Start camera stream
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    print("Server running at http://<pi-ip>:8000")
    server.serve_forever()
finally:
    picam2.stop_recording()
