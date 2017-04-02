# -*- coding: utf-8 -*-
import socket
import sys
import time
import hashlib
import os
import math

#constant Variables
s = None
address = None
PACKET_SIZE = 1000
WINDOW_SIZE = 1

def main():
    global s, address
    if len(sys.argv) != 3:
        print("Incorrect number of arguments. Please enter IP:port and window size!")
        sys.exit()
    arg_split = sys.argv[1].split(':')
    host = arg_split[0]
    if '.' in host:
        host = socket.gethostbyname(host)
    port = int(arg_split[1])
    size = int(sys.argv[2])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print ("Failed to create socket")

    address = (host,port)


    while True:
        connect(address)

        list = ["transform", "disconnect"]
        temp = raw_input("Command: ")
        inputs = temp.split(" ")
        if inputs[0] not in list:
            print("Command not recognized!")
            temp = raw_input("Command: ")
            inputs = temp.split(" ")
        if inputs[0] == "disconnect":
            print("Disconnecting from reldat-server...")
            sys.exit()

        F = inputs[1]
        data = None
        #read downloaded file
        if checkFile(F) != -1:
            data = makePackets(F)

        #still fixing this part, need to include sequence numbers
        s.sendto(data, address)
        s.recvfrom(data,address)
        print(data)

    s.close

#make packets for sending
def makePackets(fileName):
    packets = []
    with open(fileName, 'rb') as f:
        fileSize = os.path.getsize(fileName)
        numOfPackets = (fileSize/PACKET_SIZE) + 1
        packetData = f.read(PACKET_SIZE)
        packets.append(packetData)
        print(packets)
    return packets

#check if file contains ascii characters only and is in the right directory
def checkFile(fileName):
    if os.path.isfile(fileName):
        with open(fileName, 'rb') as f:
            text = f.read().replace('\n', '')
        try:
            text.encode('ascii')
        except UnicodeDecodeError:
            print ("File should contain ascii characters")
            return -1
        f.close()
    else:
        print("File does not exist in directory!")
        return -1

def checkSum(msg, checkMsg):
    global sock, address
    message = hashlib.md5()
    message.update(checkMsg)
    checkSumData = message.hexdigest()
    if checkSumData == msg:
        return True
    else:
        return False

def connect(address):
    try:
        # handshake between client and server
        s.sendto("SYN", address)
        data, addr = s.recvfrom(PACKET_SIZE)
        if data == "SYNACK":
            print("Client received " + data + ", sending ACK")
            s.sendto("ACK", address)
        print("Successful connection with reldat-server!")
    except socket.error:
        print ("Failed to connect with reldat-server!")
        sys.exit()

if __name__ == "__main__":
    main()




