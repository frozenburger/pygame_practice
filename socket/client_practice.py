import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
SERVER = "192.168.0.27"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    global client
    message = msg.encode(FORMAT)

    # configure header aka. message length in string format
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # pad heaader so that it is 64 bytes
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

send("Hello World!")
send("Hello Everyone!")
send("Hello Tim!")
send(DISCONNECT_MESSAGE)