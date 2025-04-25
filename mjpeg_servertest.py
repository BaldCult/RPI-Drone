#!/usr/bin/python3

import io
import logging
import socketserver
import asyncio
import json
from http import server
from threading import Condition, Thread

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

import telemetry
import gamepad_test  # Imports joystick values

PAGE = """\
<html>
<head>
<link rel="stylesheet" href="style.css">
<title>RPI-Drone</title>
</head>
<body>
<div class="topnav">
  <a href="https://github.com/BaldCult/RPI-Drone">GitHub</a>
</div>
<h1>RPI-Drone</h1>
<img src="stream.mjpg" width="640" height="480" /><br><br>

<div id="joystick-box">
<h2>Joystick Values:</h2>
<p>Left Stick: X = <span id="lx">0</span>, Y = <span id="ly">0</span></p>
<p>Right Stick: X = <span id="rx">0</span>, Y = <span id="ry">0</span></p>
</div>

<div id="telemetry-box">
<h2>Telemetry Values:</h2>
<p>Acceleration: X = <span id="ax">0</span>, Y = <span id="ay">0</span>, Z = <span id="az">0</span></p>
<p>Gyro: X = <span id="gx">0</span>, Y = <span id="gy">0</span>, Z = <span id="gz">0</span></p>
<p>Temperature: <span id="temp">0</span></p>
</div>

<script>
function fetchJoystick() {{
    fetch('/joystick.json')
        .then(response => response.json())
        .then(data => {{
            document.getElementById('lx').textContent = data.left_X;
            document.getElementById('ly').textContent = data.left_Y;
            document.getElementById('rx').textContent = data.right_X;
            document.getElementById('ry').textContent = data.right_Y;
        }})
        .catch(err => console.error("Joystick fetch error:", err));
}}

function fetchTelemetry() {{
    fetch('/telemetry.json')
        .then(response => response.json())
        .then(data => {{
            document.getElementById('ax').textContent = data.acceleration.x;
            document.getElementById('ay').textContent = data.acceleration.y;
            document.getElementById('az').textContent = data.acceleration.z;
            document.getElementById('gx').textContent = data.gyro.x;
            document.getElementById('gy').textContent = data.gyro.y;
            document.getElementById('gz').textContent = data.gyro.z;
            document.getElementById('temp').textContent = data.temperature;
        }})
        .catch(err => console.error("Telemetry fetch error:", err));
}}

setInterval(fetchJoystick, 10);
setInterval(fetchTelemetry, 10);
</script>

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
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
          elif self.path == '/style.css':
            css = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/css')
            self.send_header('Content-Length', len(css))
            self.end_headers()
            self.wfile.write(css)
        elif self.path == '/joystick.json':
            # Return the latest joystick values as JSON
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(gamepad_test.latest_values).encode('utf-8'))
        elif self.path == '/telemetry.json':
            # Return the latest telemetry values as JSON
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(telemetry.latest_values).encode('utf-8'))
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
def start_telemetry_reader():
    asyncio.run(telemetry.read_gyro_data())

joystick_thread = Thread(target=start_joystick_reader, daemon=True)
telemetry_thread = Thread(target=start_telemetry_reader, daemon=True)
telemetry_thread.start()
joystick_thread.start()

# Start camera stream
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    print("Server running at http://<your-pi-ip>:8000")
    server.serve_forever()
finally:
    picam2.stop_recording()
