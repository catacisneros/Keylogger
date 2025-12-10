#!/usr/bin/env python3
"""
Web Server - Serves a web interface for input and forwards it to the display terminal
"""
from flask import Flask, render_template_string, request
import socket
import threading
import time

app = Flask(__name__)

# Socket connection to display terminal
display_socket = None
socket_lock = threading.Lock()

def connect_to_display_terminal(host='localhost', port=12345):
    """Connect to the display terminal"""
    global display_socket
    while True:
        try:
            with socket_lock:
                if display_socket is None:
                    display_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    display_socket.connect((host, port))
                    print(f"Web server connected to display terminal at {host}:{port}")
        except ConnectionRefusedError:
            print(f"Waiting for display terminal to start on {host}:{port}...")
            time.sleep(2)
        except Exception as e:
            print(f"Connection error: {e}")
            time.sleep(2)

# Start connection thread
connection_thread = threading.Thread(target=connect_to_display_terminal, daemon=True)
connection_thread.start()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Input</title>
</head>
<body>
    <textarea id="inputField" style="width: 100%; height: 100vh; font-size: 16px; padding: 10px; border: none; outline: none;"></textarea>
    <script>
        const inputField = document.getElementById('inputField');
        let lastLength = 0;

        function sendInput(text) {
            fetch('/input', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            }).catch(() => {});
        }

        inputField.addEventListener('input', function(e) {
            const currentLength = e.target.value.length;
            if (currentLength > lastLength) {
                sendInput(e.target.value.slice(lastLength));
            } else if (currentLength < lastLength) {
                sendInput(e.target.value);
            }
            lastLength = currentLength;
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/input', methods=['POST'])
def receive_input():
    """Receive input from web interface and forward to display terminal"""
    global display_socket
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if text:
            with socket_lock:
                if display_socket:
                    display_socket.sendall(text.encode('utf-8'))
                    return {'status': 'success'}, 200
                else:
                    return {'status': 'error', 'message': 'Not connected to display terminal'}, 503
        return {'status': 'success'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

@app.route('/status')
def status():
    """Check connection status to display terminal"""
    global display_socket
    with socket_lock:
        connected = display_socket is not None
        if connected:
            try:
                # Try to send a test packet (non-blocking check)
                display_socket.getpeername()
                return {'connected': True}, 200
            except:
                display_socket = None
                return {'connected': False}, 200
        return {'connected': False}, 200

if __name__ == '__main__':
    print("Starting web server...")
    print("Open http://localhost:8080 in your browser")
    print("Make sure display_terminal.py is running first!")
    app.run(host='0.0.0.0', port=8080, debug=False)

