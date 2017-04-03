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

    
    while True:
        expected_seq_num = 1
        ackNum = 0

        # Establish connection via receiving of packet and sending of ACK
        connect()
        

    s.close()

def connect():
    # implementing handshake between client and server
    while True:
        try:
            packet, addr = s.recvfrom(PACKET_SIZE)
            #checksum, data = data.split(',',1)
            #s.settimeout(None)
        
            header = decodeHeader(packet)
            if expected_seq_num > header[0]:
                print("Packet is out of order")
            else:
                # transform data
                header.isUpper()
                print(packet)

            checkData = checkSum(data)
            
            if checkSumCheck(header[4], checkData):
                if header[0] == expected_seq_num:
                    print("Server received " + data + ", sending ACK")
                    ## Need to change ACK value in header ##
                        
                    s.sendto(checkData, addr)
                    expected_seq_num = expected_seq_num +1

            else:
                # discard packet and resend ACK
                print("Packet was discarded do to error")
                
        except socket.error:
            print("Failed to connect with reldat-client")
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

def packetACKHeader(packets):
    seqNum = 0
    ackNum = 1
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
        #ackNum += 1
    return packetHeader

if __name__ == "__main__":
    main()
