#!/usr/bin/env python3
import socket
from multiprocessing import Pool

# CONSTANTS
OUTBOUND_HOST = "127.0.0.1"
OUTBOUND_PORT = 8001
OUTBOUND_BUFFER_SIZE = 1024
PAYLOAD_URL = "www.google.com"
PAYLOAD = f"GET / HTTP/1.0\r\nHost: {PAYLOAD_URL}\r\n\r\n"

def main(_):
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # Connect to the proxy server
        s.connect((OUTBOUND_HOST, OUTBOUND_PORT))

        # Send the payload to the proxy server
        s.sendall(PAYLOAD.encode())

        peer_addr = s.getpeername()
        # No longer write/send
        s.shutdown(socket.SHUT_WR)

        # Reading data until no more left
        data = b""
        while True:
            fetched_data = s.recv(OUTBOUND_BUFFER_SIZE)
            if not fetched_data:
                break
            data += fetched_data

        print("Received From:", str(peer_addr[0]) + ":" + str(peer_addr[1]), "Content:", data)

if __name__ == "__main__":
    with Pool() as p:
        p.map(main, [None for i in range(10)])