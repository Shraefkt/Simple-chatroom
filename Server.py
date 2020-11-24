import socket
import threading
import re
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER,PORT)
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECTED"
NICKNAME_MSG = "N/"
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDRESS)
display = []
conns = []
Nickname = {}
def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    name = addr
    while connected:
        for message in display:
            conn.send(f"\n{message}".encode(FORMAT))
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            if re.findall(f"^{NICKNAME_MSG}", msg):
                Nickname[addr] = msg.split(NICKNAME_MSG)[1]
                name = Nickname[addr]
            else:
                user_message = f"[{name}] {msg}"
                display.append(user_message)
            user_message = f"[{name}] {msg}"
            print(user_message)

    conn.close()

def start():
    print("[STARTING] server is starting...")
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        conn,addr = server.accept()
        thread = threading.Thread(target = handle_client,args = (conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



start()
