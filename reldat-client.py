import socket
import sys
import time


def main():
    if len(sys.argv) > 5:
        print("Command line arguments incorrect!")

    if sys.argv[1] == "transform":
        F = sys.argv[2]
    if sys.argv[1] == "disconnect":
        print("Disconnecting from reldat-server!")
        sys.exit()
    arg_split = sys.argv[1].split(':')
    host = arg_split[0]
    port = int(arg_split[1])
    windowSize = sys.argv[2]
