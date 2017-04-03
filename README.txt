
Name:
Zhang Wan
Jarred Aultman

Files:
-reldat-client.py

-reldat-server.py

-README.txt
The README file contains the details of our design of the reliable data transfer protocol and instructions on how to compile and run our program.
 
-sample.txt
The sample text file contains a sample output of the execution of our RDT protocol.

DESIGN DOCUMENTATION:
The design report will need to describe at least the following:
● A high level description of how RELDAT works along with any special features that youmay have designed and implemented.● A detailed description of the RELDAT header structure and its header fields.

-Source Port
-Destination Port
-Length
-Checksum
-Sequence Number
-ACK Number
-Window Size
● Finite-state machine diagrams for the two RELDAT end-points.● Algorithmic descriptions for any non-trivial RELDAT functions.

Please make sure that you provide a clear answer to (at least) the following questions in your report:● How does RELDAT perform connection establishment and connection termination?● How does RELDAT detect and deal with duplicate packets?● How does RELDAT detect and deal with corrupted packets?● How does RELDAT detect and deal with lost packets?● How does RELDAT detect and deal with re-ordered packets?
● How does RELDAT support bi-directional data transfers?● How does RELDAT provide byte-stream semantics?● Are there any special values or parameters in your design (such as a minimum packetsize)?