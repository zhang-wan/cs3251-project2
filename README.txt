
Name:
Zhang Wan
Jarred Aultman

Files:
-reldat-client.py
The client side of the GBN RELDAT project.

-reldat-server.py
The server side of the GBN RELDAT project.

-README.txt
The README file contains the details of our design of the reliable data transfer protocol and instructions on how to compile and run our program.
 
-sample.txt
The sample text file contains a sample output of the execution of our RDT protocol.

DESIGN DOCUMENTATION:
The design report will need to describe at least the following:
● A high level description of how RELDAT works along with any special features that youmay have designed and implemented.

Helper Functions:
-packetHeader(packets): establishes the header for each packet
-decodeHeader(packet): helps parse through the packet header to pull or modify variables
-checksum(data): constructs the checksum for the data of the packet utilizing the hash library
-checkSumCheck(checksum, data_to_check): helps determine if checksum expected matches what was sent by the client. This assists with detecting corrupt or lost packets
● A detailed description of the RELDAT header structure and its header fields.

-Checksum
-Sequence Number
-ACK Number
-Window Size
-Payload

● Finite-state machine diagrams for the two RELDAT end-points.
● Algorithmic descriptions for any non-trivial RELDAT functions.

Please make sure that you provide a clear answer to (at least) the following questions in your report:● How does RELDAT perform connection establishment and connection termination?

A socket is created in both the server and the client. The connection is established based on the host name and/or IP address and port.
● How does RELDAT detect and deal with duplicate packets?

The RELDAT server will discard any packet that has a matching checksum and sequence number to the expected respective checksum and sequence number. The server will resend last ACK’d packet until client times out and resends appropriate packet.
● How does RELDAT detect and deal with corrupted packets?

RELDAT will check the checksum calculated using the hash library for corrupted packets. If the checksum extracted from the header sent to the server does not match the calculated checksum of the data sent on the server side, then the packet is discarded and the last ACK is sent back to the client. The client will then resend the last packet (the corrupted one). 
● How does RELDAT detect and deal with lost packets?

The server will continue to receive packets but will discard them and resend the ACK for the last packet received and acknowledged successfully. If the sequence number of the incoming packet does not match the expected sequence number then we assume the packet is lost and will continue to resend the last ACK until the client times out and resends the correct packet.

RELDAT will keep track of the expected sequence number within the server. When an incoming packet is received in the server, if its sequence number does not match the expected number, the packet will be discarded and it resends the ACK of the expected packet (packet with highest in-order sequence number) to the client.
● How does RELDAT detect and deal with re-ordered packets?

The server ignores packets until the highest in-order sequence number is sent by the client. Once it is matched, server sends an ACK for that packet and continues receiving packets.

● How does RELDAT support bi-directional data transfers?

There is no control or wait implemented to keep data from being transferred from client to server and vice versa
● How does RELDAT provide byte-stream semantics?● Are there any special values or parameters in your design (such as a minimum packetsize)?