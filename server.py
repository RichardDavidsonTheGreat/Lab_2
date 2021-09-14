#!/usr/bin/env python3
import socket
import time
from multiprocessing import Pool

#{<protocol>, <src addr>, <src port>, <dest addr>, <dest port>}

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        
        #bind socket to address
        s.bind((HOST, PORT))
        
        print(s.getsockname())

        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            
            #recieve data, wait a bit, then send it back
            full_data = conn.recv(BUFFER_SIZE)
            time.sleep(0.5)
            print(full_data)
            
            conn.sendall(full_data)
            print(conn.recv(BUFFER_SIZE))
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()



if __name__ == "__main__":
    main()