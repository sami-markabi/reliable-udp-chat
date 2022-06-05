from socket import *
from xmlrpc import server
import zlib
import time
serverPort = 12000
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

while True:
    clientAddress=("127.0.0.1",47878)
    message1 = recievepkt(2048,clientAddress)
    if message1=='Hello' :
        message2=input('Connect to ' +clientAddress[0]+ '?')
        if message2=='Yes' or message2 == 'yes':
            sendpacket('ACK',clientAddress)
            while (message2!='exit'):
                message1=recievepkt(2048,clientAddress)
                if (message1=='exit'):
                    break
                print('<user 1>: '+ message1)
                message2=input('<user 2>: ')
                sendpacket(message2,clientAddress)
                if message2=='exit':	
                    print('user 2 ended chat')
        else:
            print('user 2 not connected')
