import socket
import threading
from ecies.utils import generate_key
from ecies import encrypt, decrypt

HEADER = 2
PORT = 30522
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'ascii'
DISCONNECT_MESSAGE = "Exit"
INTRO_MESSAGE = "P2PEM"
CAPABILITIES = [
    "text:0.0.1",
    "sha256:0.0.1",
    "aes-256-ctr:0.0.1",
    "secp256k1:0.0.1"
    ]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print(f"[{addr}] has disconnected.")
                exit()
            elif msg == INTRO_MESSAGE:
                print(f"\nIncoming introduction message: {msg}")
                print("Sending introduction message.")
                conn.send(INTRO_MESSAGE.encode(FORMAT))
                print("Introduction complete.")
            elif msg == CAPABILITIES:
                conn.send(CAPABILITIES.encode(FORMAT))
            else:
                print(f"[{addr}] {msg}")
            message = input("Enter message: ")
            if message == DISCONNECT_MESSAGE:
                print("Closing the server.")
                bye = "Closing the server. Bye."
                conn.send(bye.encode(FORMAT))
            else:
                conn.send(message.encode(FORMAT))

    conn.close()


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()


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