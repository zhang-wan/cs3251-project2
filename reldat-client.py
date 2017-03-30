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
    global s, address
    if len(sys.argv) > 3 or len(sys.argv) != 3:
        print("Incorrect arguments. Please enter IP:port and window size!")
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
        temp = raw_input("Command: ")
        command = temp.split(" ")
        while command[0] != "transform" and command[0] != "disconnect":
            print("Command not recognized!")
            temp = raw_input("Command: ")
            command = temp.split(" ")
        if command[0] == "disconnect":
            print("Disconnecting from reldat-server...")
            sys.exit()

        F = command[1]
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
            return -1
    else:
        print("File does not exist in directory!")
