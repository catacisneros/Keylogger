## display_terminal.py (The Receiver)
- Listens on port 12345 for connections.
- When connected, receives characters one at a time.
- Prints each character to the terminal as it arrives.

## web_server.py (The Middleman)

### Part 1: Connection Setup (lines 16 to 35)
- Connects to the display terminal in the background.
- Retries if the display terminal isn’t running yet.

### Part 2: Web Page (lines 37 to 70)
- Serves a simple HTML page with a text box.
- JavaScript watches the text box and sends new text to the server.

### Part 3: Receiving Input (lines 76 to 93)
- When the web page sends text, receives it.
- Forwards it to the display terminal via the socket.

### Part 4: Starting the Server (lines 111 to 115)
- Starts the web server on port 8080.

## How It All Works Together
1. You run display_terminal.py → it waits for connections.
2. You run web_server.py → it connects to the display terminal and starts a web server.
3. You open http://localhost:8080 → you see a text box.
4. You type in the text box → JavaScript sends it to the web server.
5. The web server forwards it to the display terminal.
6. The display terminal prints it → you see it in your terminal.

**Simple flow:** Browser → Web Server → Display Terminal → Your Screen
