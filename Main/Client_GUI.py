import socket
import tkinter as tk
from tkinter import filedialog
import time
import threading
import os

class GUI:
    def __init__(self, ipAddr, port):
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.connect((ipAddr, port))

        self.Window = tk.Tk()
        self.Window.withdraw()

        self.login = tk.Toplevel()

        self.login.title("Login/Sign Up")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350)

        self.pls = tk.Label(self.login, 
                            text="Login to our Chat Room", 
                            justify=tk.CENTER,
                            font="Helvetica 12 bold")

        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.userLabelName = tk.Label(self.login, text="Username: ", font="Helvetica 11")
        self.userLabelName.place(relheight=0.2, relx=0.1, rely=0.25)

        self.userEntryName = tk.Entry(self.login, font="Helvetica 12")
        self.userEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.30)
        self.userEntryName.focus()

        self.roomLabelName = tk.Label(self.login, text="Room ID: ", font="Helvetica 12")
        self.roomLabelName.place(relheight=0.2, relx=0.1, rely=0.40)

        self.roomEntryName = tk.Entry(self.login, font="Helvetica 11", show="*")
        self.roomEntryName.place(relwidth=0.4 ,relheight=0.1, relx=0.35, rely=0.45)
        
        self.go = tk.Button(self.login, 
                            text="ENTER", 
                            font="Helvetica 12 bold", 
                            command = lambda: self.proceedUI(self.userEntryName.get(), self.roomEntryName.get()))
        
        self.go.place(relx=0.35, rely=0.62)

        self.Window.mainloop()


    def proceedUI(self, username, roomId=0):
        self.name = username
        self.serverSocket.send(str.encode(username))
        time.sleep(0.1)
        self.serverSocket.send(str.encode(roomId))
        
        self.login.destroy()
        self.layout()

        rcv = threading.Thread(target=self.receive) 
        rcv.start()


    def layout(self):
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="#c9c9c9")
        self.chatBoxHead = tk.Label(self.Window, 
                                    bg = "#c9c9c9", 
                                    fg = "#290054", 
                                    text = self.name , 
                                    font = "Ariel 11 bold", 
                                    pady = 5)

        self.chatBoxHead.place(relwidth = 1)

        self.line = tk.Label(self.Window, width = 450, bg = "#ABB2B9") 
		
        self.line.place(relwidth = 1, rely = 0.07, relheight = 0.012) 
		
        self.textCons = tk.Text(self.Window, 
                                width=20, 
                                height=2, 
                                bg="#242526", 
                                fg="#adb2b8", 
                                font="Helvetica 11", 
                                padx=5, 
                                pady=5) 
		
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08) 
		
        self.labelBottom = tk.Label(self.Window, bg="#ABB2B9", height=80) 
		
        self.labelBottom.place(relwidth = 1, 
							    rely = 0.8) 
		
        self.entryMsg = tk.Entry(self.labelBottom, 
                                bg = "#242526", 
                                fg = "#adb2b8", 
                                font = "Helvetica 11")
        self.entryMsg.place(relwidth = 0.74, 
							relheight = 0.03, 
							rely = 0.008, 
							relx = 0.011) 
        self.entryMsg.focus()

        self.buttonMsg = tk.Button(self.labelBottom, 
								text = "Send", 
								font = "Helvetica 10 bold", 
								width = 20, 
								bg = "#ABB2B9", 
								command = lambda : self.sendButton(self.entryMsg.get())) 
        self.buttonMsg.place(relx = 0.77, 
							rely = 0.008, 
							relheight = 0.03, 
							relwidth = 0.22) 


        self.labelFile = tk.Label(self.Window, bg="#ABB2B9", height=70) 
		
        self.labelFile.place(relwidth = 1, 
							    rely = 0.9) 
		
        self.fileLoc = tk.Label(self.labelFile, 
                                text = "Choose File to Send",
                                bg = "#2C3E50", 
                                fg = "#290054", 
                                font = "Helvetica 11")
        self.fileLoc.place(relwidth = 0.65, 
                                relheight = 0.03, 
                                rely = 0.008, 
                                relx = 0.011) 

        self.browse = tk.Button(self.labelFile, 
								text = "Browse", 
								font = "Helvetica 10 bold", 
								width = 13, 
								bg = "#ABB2B9", 
								command = self.browseFile)
        self.browse.place(relx = 0.67, 
							rely = 0.008, 
							relheight = 0.03, 
							relwidth = 0.15) 

        self.sengFileBtn = tk.Button(self.labelFile, 
								text = "Send", 
								font = "Helvetica 10 bold", 
								width = 13, 
								bg = "#ABB2B9", 
								command = self.sendFile)
        self.sengFileBtn.place(relx = 0.84, 
							rely = 0.008, 
							relheight = 0.03, 
							relwidth = 0.15)
    

        self.textCons.config(cursor = "arrow")
        scrollbar = tk.Scrollbar(self.textCons) 
        scrollbar.place(relheight = 1, 
						relx = 0.974)

        scrollbar.config(command = self.textCons.yview)
        self.textCons.config(state = tk.DISABLED)


    def browseFile(self):
        self.fileName = filedialog.askopenfilename(initialdir="/", 
                                    title="Select a file",
                                    filetypes = (("Text files", 
                                                "*.txt*"),
                                                ("all files", 
                                                "*.*")))
        self.fileLoc.configure(text="File Selected: "+ self.fileName)


    def sendFile(self):
        self.serverSocket.send("FILE".encode())
        time.sleep(0.1)
        self.serverSocket.send(str("client_" + os.path.basename(self.fileName)).encode())
        time.sleep(0.1)
        self.serverSocket.send(str(os.path.getsize(self.fileName)).encode())
        time.sleep(0.1)

        file = open(self.fileName, "rb")
        data = file.read(1024)
        while data:
            self.serverSocket.send(data)
            data = file.read(1024)
        self.textCons.config(state=tk.DISABLED)
        self.textCons.config(state = tk.NORMAL)
        self.textCons.insert(tk.END, " [ You ] "
                                     + str(os.path.basename(self.fileName)) 
                                     + " Sent\n\n")
        self.textCons.config(state = tk.DISABLED) 
        self.textCons.see(tk.END)


    def sendButton(self, msg):
        self.textCons.config(state = tk.DISABLED) 
        self.msg=msg 
        self.entryMsg.delete(0, tk.END) 
        snd= threading.Thread(target = self.sendMessage) 
        snd.start() 


    def receive(self):
        while True:
            try:
                message = self.serverSocket.recv(1024).decode()

                if str(message) == "FILE":
                    fileName = self.serverSocket.recv(1024).decode()
                    fileLen = self.serverSocket.recv(1024).decode()
                    user = self.serverSocket.recv(1024).decode()

                    if os.path.exists(fileName):
                        os.remove(fileName)

                    total = 0
                    with open(fileName, 'wb') as file:
                        while str(total) != fileLen:
                            data = self.serverSocket.recv(1024)
                            total = total + len(data)     
                            file.write(data)
                    
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, " [ " + str(user) + " ] " + fileName + " Received\n\n")
                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)

                else:
                    self.textCons.config(state=tk.DISABLED)
                    self.textCons.config(state = tk.NORMAL)
                    self.textCons.insert(tk.END, 
                                    message+"\n\n") 

                    self.textCons.config(state = tk.DISABLED) 
                    self.textCons.see(tk.END)

            except: 
                print("An error occured!") 
                self.serverSocket.close() 
                break

    def sendMessage(self):
        self.textCons.config(state=tk.DISABLED) 
        while True:  
            self.serverSocket.send(self.msg.encode())
            self.textCons.config(state = tk.NORMAL)
            self.textCons.insert(tk.END, 
                            " [ You ] " + self.msg + "\n\n") 

            self.textCons.config(state = tk.DISABLED) 
            self.textCons.see(tk.END)
            break

ipAddr = "127.0.0.1"
port = 10000
g = GUI(ipAddr, port)
