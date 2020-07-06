import socket
import threading
import CardBlitz.static_values as val

SERVER = socket.gethostbyname(socket.gethostname())
PORT = val.port
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

client_list = []

def handle_client(conn, addr):
    global client_list
    client_list.append(conn)
    connected = True
    while connected:
        header = conn.recv(val.header_len).decode(val.utf8)
        print(header)
        if header != '':
            msg_len = int(header)
            msg = conn.recv(msg_len).decode(val.utf8)
            if msg.split(',')[0] == 'move':
                print(msg)
                send_all(msg)

def send_all(msg_string):
    global client_list
    for conn in client_list:
        send_message(conn, msg_string)

def send_message(conn, msg_string):
    message = msg_string.encode(val.utf8)
    msg_len = len(message)

    # pad header into max length
    header = str(msg_len).encode(val.utf8)
    header += b' '*(val.header_len - len(header))

    conn.send(header)
    conn.send(message)


def start():
    server.listen()
    print('Listening on {}'.format(SERVER))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print('Player {} has joined.'.format(threading.activeCount()-1))

start()