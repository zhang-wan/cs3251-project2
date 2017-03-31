import socket
import sys
import time


def main():
    global sock, address
    if len(sys.argv) != 2:
        print("Incorrect number of arguments. Please enter <port number> <max window size>")
        sys.exit()
    port = sys.argv[0]
    size = sys.argv[1]

#Create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket created")
    except socket.error:
        print("Failed to create socket")
        sys.exit()
#Bind socket to host and port
    try:
        s.bind("", port)
    except:
        print("Bind failed")
        sys.exit()
    s.listen()
    while 1:
        d = s.recvfrom(size)
        data = d[0]
        addr = d[1]

        if not data:
            break
        s.close()
     
    
