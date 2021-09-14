#!/usr/bin/env python3
import socket, sys
import time
from multiprocessing import Process

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, msg):
        print(f'Failed to create socket. Error code: {str(msg[0])} , Error message : {msg[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def sendToGoogle(payload):
    try:
        host = 'www.google.com'
        port = 80

        buffer_size = 4096

        payload = payload.decode()
        

        #make the socket, get the ip, and connect
        s = create_tcp_socket()

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip , port))
        print (f'Socket Connected to {host} on ip {remote_ip}')
        
        #send the data and shutdown
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        #continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data:
                 break
            full_data += data
        #print(full_data)
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()
    return full_data

def handleSend(addr, conn):
    print("Connected by", addr)
            
    #recieve data, wait a bit, then send it back
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
        
    conn.sendall(sendToGoogle(full_data))
    conn.shutdown(socket.SHUT_RDWR)
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        
        #bind socket to address
        s.bind((HOST, PORT))
        

        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            p = Process(target = handleSend, args = (addr,conn))
            p.daemon = True
            p.start()
            print("Started Process ",p)

    
if __name__ == "__main__":
    main()