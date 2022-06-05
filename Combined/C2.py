from socket import *
from xmlrpc import server
import zlib
import time
serverPort = 47878
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', serverPort))
print ('The server is ready to receive')

def sendpacket(msg, address):
    windowlength=4
    seqnum=1
    base=seqnum
    count=0
    fragmentsize=5  #typical word length
    rounds=(len(msg)/fragmentsize)/4 +1 #rounded down extra run needed
    lastack=time.time()
    windowdata=[]
    lastacked=0
    delimiter = "|:|:|"
    while count<rounds:
        timeack=[]
        num=0
        while num<4:
            data=str(msg[(count*4+num)*fragmentsize:(count*4+num)*fragmentsize+fragmentsize])
            checksum=zlib.crc32(data.encode())#checksum checked on receiver side, no ack sent in case of errors
            packet=str(seqnum) + delimiter+ data + delimiter + str(checksum)     
            windowdata.append(packet)   #save data to be resent
            packet = str(packet).encode()
            timeack.append(time.time())
            serverSocket.sendto(packet,address)
            seqnum+=1
            if seqnum == 6:
                seqnum=1
            num+=1
        num=0
        while num<4:
            ack=serverSocket.recvfrom(2048)
            if ack[0].decode()[0:3]=="ACK": #"ACKseqnum" from receiver
                if int(ack[0].decode()[3:4])== base:
                    lastacked=base
                    base=base+1
                    lastack=time.time() #time at last ack
                    num+=1  
            if base==6:
                base=1
            if num<4 and lastack-timeack[num]>1:
                message= windowdata[(count)*4+num]
                serverSocket.sendto(message,address)
                timeack[num]=time.time()   #update sent time
        count+=1
    serverSocket.sendto("||:|".encode(),address)


def recievepkt(NumbBytes,address) :
    windowlength=4
    seqnum=1
    count=0
    delimiter = "|:|:|"
    rcvpkt ,clientaddress= serverSocket.recvfrom(NumbBytes)
    msg = ""
    while rcvpkt.decode() != "||:|":
        while count < windowlength:
            rcvpkt=rcvpkt.decode().split(delimiter)
            checksum2 = zlib.crc32(rcvpkt[1].encode())
            if rcvpkt[0] == str(seqnum) and rcvpkt[2] == str(checksum2):
                
                ack = "ACK"+str(seqnum)
                serverSocket.sendto(ack.encode(),clientaddress)
                seqnum+=1
                msg += rcvpkt[1]
                rcvpkt,clientaddress = serverSocket.recvfrom(NumbBytes)
                count +=1 
            else: break

            if seqnum == 6:
                seqnum = 1
        if count == windowlength:
            count =0
        else:       
            rcvpkt,clientaddress = serverSocket.recvfrom(NumbBytes) #triggered by break
                
    return msg








def sendfile():
    import socket               # Import socket module

    TCPsocket = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 15001                 # Reserve a port for your service.

    try:
        TCPsocket.connect((host, port))
    except :
        raise Exception("There's no receiving end...")

    fileName = input('Enter file name: ')

    f = open(fileName,'rb')
    TCPsocket.send(fileName.encode())
    print ('Sending...')
    l = f.read(1024)
    while (l):
        print ('Sending...')
        TCPsocket.send(l)
        l = f.read(1024)
    f.close()
    print ("Done Sending")
    TCPsocket.shutdown(socket.SHUT_WR)
    print (TCPsocket.recv(1024).decode())
    TCPsocket.close()


def receivefile():
    import socket               # Import socket module

    TCPsocket = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 15001                 # Reserve a port for your service.


    TCPsocket.bind((host, port))        # Bind to the port

#f = open(fileName,'wb')
    TCPsocket.listen(5)                 # Now wait for client connection.
    while True:
        c, add = TCPsocket.accept()     # Establish connection with client.
        print ('Connecting from', add)
        print ("Receiving...")
        while True:
            fileName= c.recv(1024).decode()
            f = open(fileName,'wb')
            break
        l = c.recv(1024)
        while (l):
            print ("Receiving...")
            f.write(l)
            l = c.recv(1024)
        f.close()
        print ("Done Receiving")
        c.send('Thank you for connecting'.encode())
        c.close()                # Close the connection
        break




while True:
    clientaddress=('127.0.0.1',12000)
    sendpacket('Hello', clientaddress)
    message=recievepkt(2048,clientaddress)
    if message =='ACK':
        mymessage= input('<user 1>: ')
        while mymessage!='exit':
            if (mymessage == '/SEND'):
                sendfile()
            elif (mymessage == '/RECEIVE'):
                sendpacket(mymessage,clientaddress)
                receivefile()
                mymessage= input('<user 1>: ')
            else:
                sendpacket(mymessage,clientaddress)
                message=recievepkt(2048,clientaddress)
                print('<user 2>:'+message)
                mymessage= input('<user 1>: ')
        #sendpacket(mymessage,clientaddress)
        print('user 1 ended chat')











