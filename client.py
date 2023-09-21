import socket
import select
import sys
import threading

def chat_client(conn, addr):
    print(f"Client connected: {addr}")
    client_connected = conn is not None
    try:
        while client_connected:
            print("Waiting for client message...")
            message = conn.recv(2048).decode("utf-8")
            if message:
                print(f"<{addr}>: {message}")
                conn.send("200 OK Message received.\n".encode("utf-8"))  # Adicione '\n' ao final da mensagem
            else:
                client_connected = False
    except Exception as ex:
        print("ERROR: ", ex)
    conn.close()

def user_input_handler(server):
    while True:
        message = input()  # Aguarde a entrada do usuário
        server.send(message.encode("utf-8"))  # Envie a mensagem ao servidor

ip_address = "127.0.0.1"
port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((ip_address, port))

user_input_thread = threading.Thread(target=user_input_handler, args=(server,))
user_input_thread.daemon = True
user_input_thread.start()

running = True
while running:
    socket_list = [server]
    
    rs, ws, es = select.select(socket_list, [], [])
    if es:
        print("ERR:", es)
    if ws:
        print("WRT:", ws)
    for sock in rs:
        if sock == server:
            message = sock.recv(2048).decode("utf-8")
            print(message)