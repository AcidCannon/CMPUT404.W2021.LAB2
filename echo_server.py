#!/usr/bin/env python3
import socket

# CONSTANTS
INBOUND_HOST = "" # Listen for all possible hosts
INBOUND_PORT = 8001
INBOUND_BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Set socket option, here, reuse the same bind port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind socket to address
        s.bind((INBOUND_HOST, INBOUND_PORT))

        # Set to listening mode
        s.listen(2)

        # Continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by:", str(addr[0]) + ":" + str(addr[1]))
            # Accepted connection
            with conn:
                data = conn.recv(INBOUND_BUFFER_SIZE)
                conn.sendall(data)

if __name__ == "__main__":
    main()