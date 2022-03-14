import socket
clientSocket = socket.socket()
hostName = socket.gethostname()
IP = socket.gethostbyname(hostName)

port = 10000
 
print('Client IP: ',IP)
hostName = input('Enter friend\'s IP address:')

name = input('Enter name: ')

clientSocket.connect((hostName, port))
 
clientSocket.send(name.encode())
serverName = clientSocket.recv(1024)
serverName = serverName.decode()
 
print(serverName,' has joined...')
while True:
    message = (clientSocket.recv(1024)).decode()
    print(serverName, ":", message)
    message = input("Me : ")
    clientSocket.send(message.encode())
