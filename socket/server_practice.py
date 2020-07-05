import socket
import threading

PORT = 5050
HEADER = 64
SERVER = socket.gethostbyname(socket.gethostname())
#  a tuple is required when binding
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

# set type of connection and transfer method
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print("[NEW CONNECTION] {} connected".format(addr))

    connected = True
    while connected :
        # blocking line : waits for a message
        # use headers to determine length of message
        # always encode/decode when sending/receiving
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length != '':
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            # cleanly disconnect, aka let the server know when client disconnects
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print('[{}] : {}'.format(addr, msg))
            conn.send("Msg received".encode(FORMAT))
    conn.close()



def start():
    server.listen()
    print('[LISTENING] server is listening on {}'.format(SERVER))
    while True:
        # blocking line : accept() waits for connection, returns connection and address
        conn, addr = server.accept()
        # execute function from a new thread
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print("[CONNECTIONS] Active connections = {}".format(threading.activeCount() - 1))

print("[STARTING] server is starting...")
start()
