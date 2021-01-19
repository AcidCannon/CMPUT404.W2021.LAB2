#!/usr/bin/env python3
import socket

# CONSTANTS
OUTBOUND_HOST = "www.google.com"
OUTBOUND_PORT = 80
OUTBOUND_BUFFER_SIZE = 1024
PAYLOAD = f"GET / HTTP/1.0\r\nHost: {OUTBOUND_HOST}\r\n\r\n"

def main():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Connect to the target server
        s.connect((socket.gethostbyname(OUTBOUND_HOST), OUTBOUND_PORT))

        # Send the payload to the server
        s.sendall(PAYLOAD.encode())
        
        # No longer write/send
        s.shutdown(socket.SHUT_WR)

        # Reading data until no more left
        data = b""
        while True:
            fetched_data = s.recv(OUTBOUND_BUFFER_SIZE)
            if not fetched_data:
                break
            data += fetched_data
        
        print("Content:", data)

if __name__ == "__main__":
    main()