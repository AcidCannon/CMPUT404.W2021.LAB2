#!/usr/bin/env python3
import socket
from multiprocessing import Process

# CONSTANTS
INBOUND_HOST = "" # Listen for all possible hosts
INBOUND_PORT = 8001
INBOUND_BUFFER_SIZE = 1024
OUTBOUND_HOST = "www.google.com"
OUTBOUND_PORT = 80
OUTBOUND_BUFFER_SIZE = 1024 

def send_to_target(proxy_s, conn, client_data):
    print("Connecting to:", socket.gethostbyname(OUTBOUND_HOST) + ":" + str(OUTBOUND_PORT))
    proxy_s.sendall(client_data)
    proxy_data = b""
    while True:
        fetched_data = proxy_s.recv(OUTBOUND_BUFFER_SIZE)
        if not fetched_data:
            break
        proxy_data += fetched_data
    peer_addr = proxy_s.getpeername()
    print("Response from:", str(peer_addr[0]) + ":" + str(peer_addr[1]), "Content:", proxy_data)
    conn.sendall(proxy_data)

def main():
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        # Set socket options, here, reuse the same bind port
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
                # Fetch data from client
                client_data = conn.recv(INBOUND_BUFFER_SIZE)
                # Then send the client data to the target server
                # Create a socket object
                print("Received From:", str(addr[0]) + ":" + str(addr[1]), "Content:", client_data)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_s:
                    # Connect to the target server
                    proxy_s.connect((socket.gethostbyname(OUTBOUND_HOST), OUTBOUND_PORT))
                    p = Process(target=send_to_target, args=(proxy_s, conn, client_data))
                    p.daemon = True
                    p.start()
                    print("Start process:", p.pid)

if __name__ == "__main__":
    main()
