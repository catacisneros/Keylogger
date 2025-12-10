#!/usr/bin/env python3
"""
Display Terminal - Run this in one terminal to see input from the input terminal
"""
import socket
import sys

def display_server(host='localhost', port=12345):
    """Server that receives and displays input from the input terminal"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Display terminal ready. Waiting for connection on {host}:{port}...")
        print("=" * 50)
        
        while True:
            client_socket, address = server_socket.accept()
            print(f"\nConnected to input terminal at {address}")
            print("=" * 50)
            print("Input from other terminal will appear below:\n")
            
            try:
                while True:
                    # Receive data character by character for real-time display
                    data = client_socket.recv(1).decode('utf-8')
                    if not data:
                        break
                    # Print received character immediately
                    print(data, end='', flush=True)
            except ConnectionResetError:
                print("\n\nConnection closed. Waiting for new connection...")
                print("=" * 50)
            finally:
                client_socket.close()
                
    except KeyboardInterrupt:
        print("\n\nShutting down display terminal...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    display_server()

