# -*- coding: utf-8 -*-
import socket
import sys
import time
import hashlib
import os
s = None
address = None
MAX_PAYLOAD = 1000

def main():
    global sock, address
    if len(sys.argv) != 3:
        print("Incorrect number of arguments. Please enter IP:port and window size!")
        sys.exit()
    arg_split = sys.argv[1].split(':')
    host = arg_split[0]
    if '.' in host:
        host = socket.gethostbyname(host)
    port = int(arg_split[1])
    window_size = int(sys.argv[2])
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print("Successful connection with reldat-server!")
    except socket.error:
        print ("Failed to connect with reldat-server!")
        sys.exit()

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
        #read downloaded file
        dlFile = readFile(F)

    sock.close()

def readFile(fileName):
    if os.path.isfile(fileName):
        with open(fileName, 'r') as f:
            text = f.read().replace('\n', '')
        try:
            text.encode('ascii')
            return text
        except UnicodeDecodeError:
            print ("File should contain ascii characters")
    else:
        print("File does not exist in directory!")



#def connect(host, addr):
    #connection = False


def checkSumSend(msg):
    global s, address
    message = hashlib.md5()
    message.update(msg)
    checkSumData = message.hexdigest()
    s.sendto(checkSumData, address)


    '''while True:
        #using time library to set timeout function
        start = time.time()
        msg = "hi there"

        try:
            s.sendto(msg, address)
            receive = s.recvfrom(1024)
            receivedData = receive[0]
            addr = receive[1]
            print("Response from server: " + receivedData)


    #if no response from server after 2s
        except socket.timeout:
            ping = ping + 1
            if ping == 3:
                break
            print("The server has not answered in the last two seconds. retrying...")

    print("Timeout after 3 attempts...")
    s.close'''

if __name__ == "__main__":
    main()


