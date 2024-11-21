# This is the client program

# Sequence:
#
# 1. Create a socket
# 2. Connect it to the server process. 
#	We need to know the server's hostname and port.
# 3. Send and receive data 


import socket # include socket
import threading #include threading
person= input ("Enter name: ") 
# create a socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# The first argument AF_INET specifies the addressing family (IP addresses)
# The second argument is SOCK_STREAM for TCP service
#    and SOCK_DGRAM for UDP service

# connect to the server 
host='10.196.8.172' #use server's IP address
port=43389  # this is the server's port number, which the client needs to know
client.connect((host, port))

def receive(): # read thread
    while(True):
        try:
            message = client.recv(1024).decode()
            if message =="name": 
                client.send(person.encode("UTF-8"))
            elif message=="":
                continue  
            else:
                print(message) 
        except:
            print("Left the room ") 
            client.close() 
            break 
        
def take_input(): #write thread 
    while(True):
        val=input() # write your message here 
        message = f'{person}: {val}'
        client.send(message.encode('utf-8'))
        if(val=="/q"):  
            client.close() 
            break
    
recievethread = threading.Thread(target = receive) # The receive thread will run the receive function 
recievethread.start()
writethread = threading.Thread(target = take_input) # the write thread will run the write function
writethread.start()
