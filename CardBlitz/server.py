import socket
import threading
import CardBlitz.static_values as val

SERVER = socket.gethostbyname(socket.gethostname())
PORT = val.port
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    connected = True
    while connected:
        header = conn.recv(val.header_len).decode(val.utf8)
        if header != '':
            msg_len = int(header)
            msg = conn.recv(msg_len).decode(val.utf8)
            print(msg)


def start():
    server.listen()
    print('Listening on {}'.format(SERVER))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print('Player {} has joined.'.format(threading.activeCount()-1))

start()