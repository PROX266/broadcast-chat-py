import socket
import threading

clients = []
client_lock = threading.Lock()

def broadcast(message, sender_socket):
    with client_lock:
        for client in clients:
            if client != sender_socket:
                try:
                    client.send(message.encode("utf-8"))
                except:
                    pass

def handle_client(client_socket, client_address):
    print(f"Клиент {client_address} подключён")
    
    client_socket.send("Добро пожаловать в чат!".encode("utf-8"))
    broadcast(f"Клиент {client_address} присоединился к чату", client_socket)

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode("utf-8")
            print(f"От {client_address} пришло: {message}")
            
            broadcast(f"{client_address}: {message}", client_socket)
        except:
            break

    with client_lock:
        if client_socket in clients:
            clients.remove(client_socket)
    
    client_socket.close()
    print(f"Клиент отключился: {client_address}")
    broadcast(f"Клиент {client_address} покинул чат", None)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("127.0.0.1", 5001))
server_socket.listen()
print("Сервер запущен и ждёт подключения...")

while True:
    client_sock, client_addr = server_socket.accept()
    
    with client_lock:
        clients.append(client_sock)

    thread = threading.Thread(target=handle_client, args=(client_sock, client_addr), daemon=True)
    thread.start()