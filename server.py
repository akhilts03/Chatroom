#authors: Akhil Thirukonda Sivakumar + Amit Sonaje
#Roll nos: 2103106 + 2103107 


# This is the Server program
# Sequence of steps:
#	1. create a "welcome" socket for listening to new connections 
#	2. bind the socket to a host and port
#	3. start listening on this socket for new connections
#	4. accept an incoming connection from the client
#   5. send and receive data over the "connection" socket


import socket
from _thread import *

#  create a socket for listening to new connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				# use SOCK_STREAM for TCP
				# use SOCK_DGRAM for UDP

# bind it to a host and a port
host = '10.196.8.172' #use your own networks IP address
port = 43389  # arbitrarily chosen non-privileged port number
s.bind((host,port))
print("Server started...listening for connections")

s.listen(100)

clientlist = [] #list of all server sockets connected to the clients. 

def clientthread(conn,addr):
    conn.send("welcome to the chatroom!".encode('utf-8'))
    
    while True: 
        try:
            message = conn.recv(2048) 
            if message:
                print("<"+addr[0]+">"+message) # this is printed on the server
                
                message_to_send = "<" + addr[0] + ">" + message # this is broadcasted to all participants in the chat room
                broadcast(message_to_send, conn) # broadcasted on the connection => sent to everyone connected. 
            else:
                clientlist.remove(conn)
        except:
            continue

def broadcast(message, connection):
    for clients in clientlist:
        if clients != connection:
            try:
                clients.send(message.encode('utf-8'))
            except:
                clients.close()
                # if the link is broken, we remove the client
                remove(clients)

def remove(connection):
    if connection in clientlist:
        clientlist.remove(connection)


while True:
    
    conn,addr = s.accept()
    clientlist.append(conn)
    print(addr[0]+" " + "connected")
    
    start_new_thread(clientthread,(conn,addr))

