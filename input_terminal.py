#!/usr/bin/env python3
"""
Input Terminal - Run this in another terminal to send input to the display terminal
"""
import socket
import sys
import termios
import tty

def get_char():
    """Read a single character from stdin without requiring Enter"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def input_client(host='localhost', port=12345):
    """Client that sends user input to the display terminal in real-time"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        print(f"Connected to display terminal at {host}:{port}")
        print("Type your input below (Ctrl+C to exit):\n")
        
        try:
            while True:
                # Read a single character
                char = get_char()
                
                # Handle Ctrl+C (ASCII 3)
                if ord(char) == 3:
                    print("\n\nDisconnecting...")
                    break
                
                # Handle Enter key (ASCII 13 or 10)
                if ord(char) == 13 or ord(char) == 10:
                    char = '\n'
                
                # Send character to display terminal immediately
                client_socket.sendall(char.encode('utf-8'))
                
                # Also echo the character locally (optional - comment out if you don't want local echo)
                sys.stdout.write(char)
                sys.stdout.flush()
                
        except KeyboardInterrupt:
            print("\n\nDisconnecting...")
        finally:
            client_socket.close()
            
    except ConnectionRefusedError:
        print(f"Error: Could not connect to display terminal at {host}:{port}")
        print("Make sure display_terminal.py is running first!")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    input_client()

