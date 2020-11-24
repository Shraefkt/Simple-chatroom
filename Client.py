
from tkinter import messagebox
import threading
import tkinter as tk
import socket
import time

HEADER = 64
PORT = 5050
CLIENT = socket.gethostbyname(socket.gethostname())
SERVER = "192.168.1.149"
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECTED"
ADDRESS = (SERVER,PORT)
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDRESS)

def on_closing():
        send_message(DISCONNECT_MSG)
def display_receive():
    try:
        #print(client.recv(2048).decode(FORMAT))
        a = client.recv(2048).decode(FORMAT)
        global display
        display = []
        display = [a.split("\n")]
    except:
        print("Server/client error")
def send_message(msg):
    print("Sending message")
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b" "* (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(f"[{CLIENT}]: {message.decode(FORMAT)}")
    display_receive()
class tkpages:
    def __init__(self):
        self.mode = False
        self.colour_scheme = []
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, height=500, width=600)
        self.canvas.pack()
        self.menu_main()
        self.colour_mode()
        self.root.mainloop()
        on_closing()
    def menu_main(self):
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.homemenu = tk.Menu(self.menu, activebackground="blue", tearoff=0)
        self.menu.add_cascade(label="Menu", menu=self.homemenu)
        self.homemenu.add_command(label="Settings", command=lambda: self.settings())
        self.homemenu.add_command(label="Chatroom", command=lambda: self.GUI())
        #self.homemenu.add_command(label="Favourites", command=lambda: favourite_page())

    def GUI(self):
        self.page_setup()
        self.root.config(bg = self.colour_scheme[3])
        self.displayframe1 = tk.Frame(self.root, bg=self.colour_scheme[0], bd=15)
        self.displayframe1.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.65, anchor="n")

        self.msg_frame = tk.Frame(self.root, bg= self.colour_scheme[2], bd=10)
        self.msg_frame.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor="n")

        self.rb = tk.Button(self.msg_frame ,cursor = "exchange",relief = "solid",bg = self.colour_scheme[3], text = "🔄",fg = self.colour_scheme[1],font = ("tw cen mt condensed",30),command = lambda :self.refresh())
        self.rb.place(relheight = 1, relwidth = 0.11, relx = 0.94, anchor = "n" )

        self.entry = tk.Entry(self.msg_frame,cursor = "xterm", font=("tw cen mt condensed", 30), fg=self.colour_scheme[1], bg=self.colour_scheme[3],relief = "solid")
        self.entry.place(relwidth=0.69, relheight= 1 )

        self.sendbutton = tk.Button(self.msg_frame, cursor = "rightbutton",font=("tw cen mt condensed", 30), text="Send",bg = self.colour_scheme[1],fg = self.colour_scheme[3],
                           relief = "solid",command=lambda:self.send(self.entry.get()))
        self.sendbutton.place(relx=0.69, relheight= 1 , relwidth=0.2)

        self.scrollbar = tk.Scrollbar(self.displayframe1)
        self.scrollbar.pack(side= "right",fill = "y")
        self.mylist = tk.Listbox(self.displayframe1,fg = self.colour_scheme[4], bg = self.colour_scheme[3],yscrollcommand=self.scrollbar.set)
        self.mylist.pack(side="left", fill="both",expand = "true")
        self.scrollbar.config(command=self.mylist.yview)
    def refresh(self):
        try:
            display_receive()
        except:
            print("Error loading messages")
        try:
            self.mylist.delete(0, "end")
            for line in display:
                for l in line:
                    self.mylist.insert("end",l)
        except:
            print("error refreshing")
        print("done refreshing")

    def send(self,msg):
        send_message(msg)
        self.entry.delete(0, "end")

    def settings(self):
        self.page_setup()
        self.settingsframe = tk.Frame(self.root,bg = self.colour_scheme[0],bd = 15)
        self.settingsframe.place(relx = 0.5 ,rely = 0.05,relwidth = 0.9 , relheight = 0.9,anchor = "n")

        self.nickname_label = tk.Label(self.settingsframe,bg = self.colour_scheme[0],text = "Nickname:",font =("tw cen mt condensed", 25))
        self.nickname_label.place(relx = 0.02,rely = 0.1, relwidth = 0.25,relheight = 0.1)
        self.nickname_entry = tk.Entry(self.settingsframe,font=("tw cen mt condensed", 25))
        self.nickname_entry.place(relx = 0.3, rely =0.1, relwidth = 0.69,relheight = 0.1)

        self.nickname_button = tk.Button(self.settingsframe,relief = "solid",text = "Change",font=("tw cen mt condensed", 25),command = lambda : send_message("N/"+self.nickname_entry.get()))
        self.nickname_button.place(relx = 0.02,rely = 0.25,relwidth = 0.25,relheight = 0.15)

        self.darkmode_button = tk.Button(self.settingsframe,command = lambda :self.colour_mode(),relief = "solid",text = "Dark/Light Mode",font=("tw cen mt condensed",25))
        self.darkmode_button.place(rely = 0.8)

    def colour_mode(self):
        if self.mode == True:
            print("mode : dark")
            self.mode = False
            self.colour_scheme = ["#222831","#3E432E","#616F39","black","white"]
        else:
            print("mode :light")
            self.mode = True
            self.colour_scheme = ["white","#222831","#29465b","white","#6e7f80"]

    def changepage(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def page_setup(self):
        self.changepage()
        self.menu_main()

page = tkpages()

