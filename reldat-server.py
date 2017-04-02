import socket
import sys
import time
PACKET_SIZE = 1000

def main():
    global s, address
    if len(sys.argv) != 3:
        print("Incorrect number of arguments. Please enter <port number> <max window size>")
        sys.exit()
    port = int(sys.argv[1])
    size = int(sys.argv[2])
    host = "127.0.0.1"

    # Create a socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Socket created")
    except socket.error:
        print("Failed to create socket")
        sys.exit()

    # Bind socket to host and port
    try:
        s.bind((host, port))
    except socket.error:
        print("Bind failed")
        sys.exit()

    print("Server listening...")

    while 1:
        connect()

        #still fixing
        data, addr = s.recvfrom(PACKET_SIZE)
        s.sendto(data,addr)

    s.close()

def connect():
    # implementing handshake between client and server
    while 1:
        try:
            data, addr = s.recvfrom(PACKET_SIZE)
            s.settimeout(None)
            if data == "SYN":
                print("Server received " + data + ", sending SYNACK")
                s.sendto("SYNACK", addr)
                s.settimeout(None)
            if data == "ACK":
                print(data +" received, " + "Server is connected to client: " + str(addr))
                s.settimeout(None)
        except socket.error:
            print ("Failed to connect with reldat-client")
            sys.exit()


if __name__ == "__main__":
    main()
    
