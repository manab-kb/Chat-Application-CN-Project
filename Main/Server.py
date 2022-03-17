from http import server
import socket 
from _thread import *
from collections import defaultdict as dd
import time

rooms = dd(list)
serverSocket = socket.socket()
ipAddr = "127.0.0.1"
port = "10000"
userId = ""
roomID = ""
conn = 0
msg = ""
sendMsg = ""
fileName = ""
fileLen = ""
data = ""
total = 0

def initServer():
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def acceptConnection(ipAddr, port):
    ipAddr = ipAddr
    port = port
    serverSocket.bind((ipAddr, int(port)))
    serverSocket.listen(100)

    while True:
        conn, addr = serverSocket.accept()
        print(str(addr[0]) + " : " + str(addr[1]) + " Online")
        start_new_thread(clientThread, (conn,))
    
    serverSocket.close()

def clientThread(conn):
    userId = conn.recv(1024).decode().replace("User ", "")
    roomId = conn.recv(1024).decode().replace("Join ", "")

    if roomId not in rooms:
        conn.send("New Room Created !".encode())
    else:
        conn.send("Welcome to your Chat Room !!".encode())

    rooms[roomId].append(conn)

    while True:
        msg = conn.recv(1024)
        print(str(msg.decode()))
        if msg:
            if str(msg.decode()) == "FILE":
                sendFile(conn, roomId, userId)

            else:
                sendMsg = " [ " + str(userId) + " ] " + msg.decode()
                sendMessage(sendMsg, conn, roomId)

        else:
            remove(conn, roomId)
    
    
def sendFile(conn, roomId, userId):
    fileName = conn.recv(1024).decode()
    fileLen = conn.recv(1024).decode()
    for client in rooms[roomId]:
        if client != conn:
            try: 
                client.send("FILE".encode())
                time.sleep(0.1)
                client.send(fileName.encode())
                time.sleep(0.1)
                client.send(fileLen.encode())
                time.sleep(0.1)
                client.send(userId.encode())
            except:
                client.close()
                remove(client, roomId)

    total = 0
    print(fileName, fileLen)
    while str(total) != fileLen:
        data = conn.recv(1024)
        total = total + len(data)
        for client in rooms[roomId]:
            if client != conn:
                try: 
                    client.send(data)
                except:
                    client.close()
                    remove(client, roomId)
    print("File Sent")


def sendMessage(sendMsg, conn, roomId):
    for client in rooms[roomId]:
        if client != conn:
            try:
                client.send(sendMsg.encode())
            except:
                client.close()
                remove(client, roomId)

    
def remove(conn, roomId):
    if conn in rooms[roomId]:
        rooms[roomId].remove(conn)

initServer()
acceptConnection(ipAddr,port)
