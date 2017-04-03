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
window = []
count = 1

def main():
    global s, address
    if len(sys.argv) != 3:
        print("Incorrect number of arguments. Please enter <IP address>:<port number> <max window>")
        sys.exit()
    arg_split = sys.argv[1].split(':')
    host = arg_split[0]
    if '.' in host:
        host = socket.gethostbyname(host)
    port = int(arg_split[1])
    size = int(sys.argv[2])

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
    except socket.error:
        print ("Failed to create socket")

    address = (host,port)
    
    lastACK = time.time() # set time for for the last ACK
    num_of_ack = 0
    global next_packet_num
    next_packet_num = 0
    
    while True:

        #read downloaded file
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
            
        if checkFile(F) != -1:
            data = makePackets(F)
            numOfPackets = len(data)
            packet = packetHeader(data)

        if(next_packet_num < WINDOW_SIZE):
            try:
                # Start handshake
                print(packet)
                connect(address, packet[next_packet_num])
                next_packet_num = next_packet_num + 1
                
            except socket.timeout:
                print("Server has not responded in the last 2 seconds. Resending...")

                # Go back and resend all packets from last received ACK
                if(time.time() - lastACK > 2):
                    for i in window:
                        connect(address, window[i])
        
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

#write back to the file being transformed and renames it
def dlFile(fileName, data):
    with open(fileName, 'wb') as f:
        f.write(str(data))
    f.close
    for filename in os.listdir("."):
        if filename.startswith(fileName):
            temp = fileName.split(".")
            temp2 = temp[0]
            os.rename(fileName, temp2 +"-received"+".txt") 
    
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

# handshake between client and server
def connect(address, curr_packet):
    # SEND DATA TO SERVER
    try:
        #checkData = checkSum(curr_packet)
        s.sendto(curr_packet, address)
        # increment sequence number
        #next_packet_num = next_packet_num + 1

        # Add packet to window
        window.append(curr_packet)
    except socket.timeout:
        print ("Timeout: Server did not respond. Retrying....")
        
    # RECEIVE DATA FROM SERVER
    try:
        data, addr = s.recvfrom(PACKET_SIZE)
        checksum, data = data.split(',', 1)
        
        # Check for any errors in packet via checksum
        header = decodeHeader(data)
        if checkSumCheck(checksum, checkData) and header[1]==0:
            
            while header[0] > count:
                # reset timer
                lastACK = time.time()
                # slide window
                del window[0]
                count += 1
        else:
            print("Error was detected with received ACK")
            
        print("Successful connection with reldat-server!")
    except:
        print("Failed to connect with reldat-server!")
        sys.exit()

#packet header to store information
def packetHeader(packets):
    seqNum = 0
    ackNum = 0
    windowSize = WINDOW_SIZE
    payload = packets
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
        #ackNum += 1
    return packetHeader

def decodeHeader(packet):
    header = packet.split('|')
    seqNum = header[0]
    ackNum = header[1]
    windowSize = header[3]
    checkSum = header[4]
    payload = header[5]
    result = []
    result.append(seqNum)
    result.append(ackNum)
    result.append(windowSize)
    result.append(checkSum)
    result.append(payload)
    return result


if __name__ == "__main__":
    main()




