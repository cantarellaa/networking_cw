import socket
from ecies.utils import generate_key
from ecies import encrypt, decrypt

HEADER = 2
PORT = 30522
FORMAT = 'ascii'
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
INTRO_MESSAGE = "P2PEM"
DISCONNECT_MESSAGE = "Exit"
CAPABILITIES = [
    "text:0.0.1",
    "sha256:0.0.1",
    "aes-256-ctr:0.0.1",
    "secp256k1:0.0.1"
    ]

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    answer = client.recv(2048).decode(FORMAT)
    if answer == INTRO_MESSAGE:
        print(f"Received introduction: {answer}")
        print("Introduction complete.")
    else:
        print(answer)

print("Connected to the server, sending introduction.")
send(INTRO_MESSAGE)
# send(CAPABILITIES)

connected = True
while connected:
    message = input("Enter message: ")
    if message == DISCONNECT_MESSAGE:
        send(message)
        connected = False
    else:
        send(message)

    thing = client.recv(1024).decode(FORMAT)
    if thing == DISCONNECT_MESSAGE:
        print("Server has closed")
        connected = False
    print(thing)
client.close()


# keys = generate_key()
# data = input("Data: ")
#
# secret_key = keys.secret
# public_key = keys.public_key.format(True)
#
# encrypted_msg = encrypt(public_key, data.encode())
#
# print("Encrypted:" + encrypted_msg.hex())
#
# decrypted_msg = decrypt(secret_key, encrypted_msg)
#
# print("Decrypted:" + decrypted_msg.decode())
