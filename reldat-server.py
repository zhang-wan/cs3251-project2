import socket
import sys
import hashlib
import time

address = None
PACKET_SIZE = 1000
recv_unack = []

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

    connect()
    
    #still figuring out
    while True:
        expected_seq_num = 0
        ackNum = 0
        data, addr = s.recvfrom(PACKET_SIZE)
        print(data)
        header = decodeHeader(data)
        if expected_seq_num > header[0]:
            print("Packet is out of order")
        else:
            data.isUpper()
            print(data)

    s.close()

def connect():
    # implementing handshake between client and server
    while 1:
        try:
            data, addr = s.recvfrom(PACKET_SIZE)
            checksum, data = data.split(',',1)
            s.settimeout(None)
            if checkSumCheck(checksum, data) and data[-3:] == "SYN":
                print("Server received " + data + ", sending SYNACK")
                checkSYNACK = checkSum("SYNACK")
                s.sendto(checkSYNACK, addr)

            if checkSumCheck(checksum, data) and data[-3:] == "ACK":
                print(data +" received, " + "Server is connected to client: " + str(addr))
                break
        except socket.error:
            print ("Failed to connect with reldat-client")
            sys.exit()

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
        seqNum += 1
        ackNum += 1
    return packetHeader

if __name__ == "__main__":
    main()
