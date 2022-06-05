Project by: Mahdi Sabra, Sami Al Markabi, and Nancy Abdallah

Reliable Message Transfer

For UDP CHAT:

UDPChat Client1 and UDPChat Client2 implement a go-back-n UDP message transfer. Make sure to start Client1 before Client2 by running two terminals and entering "python3 UDPChat Client1.py". 
Once Client2 is connected, a prompt to connect to Client1 to show up, make sure to enter "Yes" to be able to connect. Messages are sent one by one, alternating between Client1 and Client2.


For TCP File transfer:

Make sure to run TCPclient1.py and TCPclient2.py in two different directories AND running the terminals in the directories of the client. 
The receiving client should be run first by entering "R" when the prompt shows up. Then run the sender client by entering "S".
After entering "S" for the sender client, a file Name prompt will show up, make sure to enter the name of the file with the extension (example: img.png).


Combined CHAT:


C1.py and C2.py are combined where it starts as a UDP chat and when a client enters "/RECEIVE" first and other enters "/SEND", a TCP connection is initiated to transfer the file. After the file transfer is completed, UDP chat will be reinitiated.

Important Remarks: 
- Client1 should always be run first
- Client1 and Client2 should be in two different directories. Terminal should be run in that directory ( example: cd ~Desktop/Client1)
- To send a file, the receiving client should be initiated first


