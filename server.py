import socket
import select
from datetime import datetime
import sys




def chat_client(conn, addr):
    print(f"Client connected: {addr}")
    client_connected = conn is not None
    client_messages = []

    try:
        while client_connected:
            print("Waiting for client message...")
            message = conn.recv(2048).decode("utf-8")

            def send_client(msg):
                conn.send(msg.encode("utf-8"))

            def ordernar():
                conn.send("Chat History \n--------------------\n".encode("utf-8"))
                for i in range(len(client_messages)):
                    conn.send((str(client_messages[i]) + "\n").encode("utf-8"))
                conn.send("--------------------\n".encode("utf-8"))
                
            def download(file_name):
                try:
                    file = open(file_name, "rb")
                    file_data = file.read(2048)
                    conn.send(file_data)
                    file.close()
                except:
                    conn.send("File not found".encode("utf-8"))

            if message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-4]
                
                if len(client_messages) >= 15:
                    client_messages.pop(0)
                    client_messages.append(str(timestamp) + " " + str(message))
                else:
                    client_messages.append(str(timestamp) + " " + str(message))

                if message == "@sair":
                    send_client("goodbye")
                    conn.close()
                    client_connected = False
                    
                elif message == "@ordernar":
                    ordernar()
                    
                elif message == "@upload":
                    send_client("Write the file name: ")
                    file_name = conn.recv(2048).decode("utf-8")
                    file = open(file_name, "wb")
                    file_data = conn.recv(2048)
                    file.write(file_data)
                    file.close()

                elif message == "@download":
                    send_client("Write the file name: ")
                    file_name = conn.recv(2048).decode("utf-8")
                    download(file_name)
                    
                elif message == "@help":
                    help_message = "@exit to exit\n@ordernar to get the last 15 messages\n@upload to upload a file\n@download to download a file already uploaded in the server\n"
                    send_client(help_message)
            else:
                client_connected = False
                
            print(f"Nao reconheço a mensagem: {message}")
            
    except Exception as ex:
        print("ERROR: ", ex)
    conn.close()


port = int(sys.argv[1]) if len(sys.argv) > 1 else 19000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(("0.0.0.0", port))

server.listen(5)

running = True
while running:
    print("Waiting for connection...")
    conn, addr = server.accept()

    chat_client(conn, addr)

server.close()
