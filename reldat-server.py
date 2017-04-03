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

    connect(address)
    while True:

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

        num_of_ack = 0
        next_packet_num = 0

        #read downloaded file
        if checkFile(F) != -1:
            data = makePackets(F)
            numOfPackets = len(data)
            packet = packetHeader(data)

            # still figuring out 
            try:
                s.settimeout(2)
                # ensure that all packets are send to server
                while num_of_ack < numOfPackets:
                    if next_packet_num < size:
                        s.sendto(packet[next_packet_num], address)
                        next_packet_num += 1
                        if next_packet_num == numOfPackets:
                            print("Successfully sent all packets!")
                        num_of_ack += 1
            except socket.timeout:
                print("Server has not responded in the last 2 seconds. Retrying...")

        data, addr = s.recvfrom(PACKET_SIZE)
        print(data)

    s.close

#make packets for sending
def makePackets(fileName):
    packets = []
    with open(fileName, 'rb') as f:
        fileSize = os.path.getsize(fileName)
        numOfPackets = (fileSize/PACKET_SIZE) + 1
        for i in range(numOfPackets):
            packetData = f.read(PACKET_SIZE)
            packets.append(packetData)
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

def checkSumCheck(checksum, data_to_check):
    message = hashlib.md5()
    message.update(data_to_check)
    checkSumData = message.hexdigest()
    if checkSumData == checksum:
        return True
    else:
        return False

def checkSum(data):
    message = hashlib.md5()
    message.update(data)
    checkSumData = message.hexdigest()
    data = checkSumData.strip() + "," + data
    return data


def connect(address):
    try:
        # handshake between client and server
        checkSYN = checkSum("SYN")
        s.sendto(checkSYN, address)
        data, addr = s.recvfrom(PACKET_SIZE)
        checksum, data = data.split(',', 1)
        if checkSumCheck(checksum, data) and data[-6:] == "SYNACK":
            print("Client received " + data + ", sending ACK")
            sendACK = checkSum("ACK")
            s.sendto(sendACK, address)
        print("Successful connection with reldat-server!")
    except socket.error:
        print ("Failed to connect with reldat-server!")
        sys.exit()

#packet header to store information
def packetHeader(packets):
    seqNum = 0
    ackNum = 0
    windowSize = 0
    payload = 0
    packetHeader = ""

    for i in packets:
        packetHeader += str(seqNum) + '|'
        packetHeader += str(ackNum) + '|'
        packetHeader += str(windowSize) + '|'
        message = hashlib.md5()
        message.update(i)
        checkSum = message.hexdigest()
        #print(checkSum)
        packetHeader += str(checkSum) + '|'
        packetHeader += str(payload)
        #packet
        seqNum += 1
        ackNum += 1
    return packetHeader


if __name__ == "__main__":
    main()


