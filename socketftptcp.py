#########################################
#Import libraries
#########################################
import socket
import os
import time
from time import sleep

#########################################
#Declaring Connection Variables
#########################################
BUFFER_SIZE = 32                                    #Buffer Size for receiving file in chunks
BUFFER_FILENAME = 1024                              #Buffer size for receiving file name
SERVER_IP = 'localhost'                             #Server IP
SERVER_PORT = 12345                                 #Server Port Number

#########################################
#Initializing UDP Socket
#########################################
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Starting server on port ',SERVER_PORT)

#########################################
#Uncomment the line below for disabling Nagle's Algortihm
#########################################

# sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

#########################################
#Uncomment the line below for disabling Delayed Ack
#########################################

# sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_QUICKACK, 1)

sock.bind((SERVER_IP, SERVER_PORT))

sock.listen(1)                                              

while True:
    print('Waiting for connection')
    connection, client_addr = sock.accept()                                 #Wait for connection

    try:
        start = time.time()                                                 #Start timer
        print(client_addr,' connected')
        file_name = connection.recv(BUFFER_FILENAME).decode()               #Receive file name     
        file_name = os.path.basename(file_name)
       
        fd = open(file_name, 'rb')                                          #Open file in read mode
        buf = fd.read(BUFFER_SIZE)                                          #Read from file equal to buffer size

        print('Sending Data')

        while(buf): 
            connection.send(buf)                                            #Send data to the client
            
            ###########################################
            # Uncomment the next line for question 4
            ###########################################
            
            #sleep(100/1000000)
            
            buf = fd.read(BUFFER_SIZE)
        
        fd.close()                                                          #Close file

        end = time.time()                                                   #End timer
        print(f"Time taken to upload: {end - start} sec")                   #Print upload time
        print(file_name," uploaded")

    finally:
        connection.close()                                                  #Close connection
        