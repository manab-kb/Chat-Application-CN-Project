import socket
serverSocket = socket.socket()
hostName = socket.gethostname()
IP = socket.gethostbyname(hostName)
 
port = 10000
 
serverSocket.bind((hostName, port))
print("Server IP: ", IP)
 
name = input('Enter name: ')
 
serverSocket.listen(1) 
 
conn, add = serverSocket.accept()
 
print('Connection Received and Established. Client: ',add[0])
 
client = (conn.recv(1024)).decode()
print(client + ' has connected.')
 
conn.send(name.encode())
while True:
    message = input('Me : ')
    conn.send(message.encode())
    message = conn.recv(1024)
    message = message.decode()
    print(client, ':', message)
