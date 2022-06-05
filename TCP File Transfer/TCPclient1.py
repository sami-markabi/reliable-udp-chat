

print("TCP File Transfer \nProject By: Sami Markabi, Mahdi Sabra, and Nancy Abdallah" )



state = input("To Send a File, Enter 'S' & To Receive a file, Enter 'R': ")

if state == 'R' or state == 'r':

    import socket               # Import socket module
    
    TCPsocket = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12000                 # Reserve a port for your service.


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

elif state == 'S' or state == 's':


    import socket               # Import socket module

    TCPsocket = socket.socket()         # Create a socket object
    host = socket.gethostname() # Get local machine name
    port = 12000                 # Reserve a port for your service.

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

else: print("Invalid input")
