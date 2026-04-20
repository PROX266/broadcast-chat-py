import socket
import threading
import sys

def receive_message(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("\nСоединение с сервером потеряно.")
                break
            print(f"\n{data.decode('utf-8')}")
            print("Введите сообщение: ", end="", flush=True)
        except:
            break
    
    print("Завершение работы потока приема...")
    client_socket.close()
    sys.exit()

def send_message(client_socket):
    while True:
        try:
            message = input("Введите сообщение: ")
            if message.lower() == 'exit':
                break
            client_socket.send(message.encode("utf-8"))
        except:
            break
    
    client_socket.close()
    sys.exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect(("127.0.0.1", 5001))
except ConnectionRefusedError:
    print("Не удалось подключиться к серверу. Убедитесь, что он запущен.")
    sys.exit()

receive_thread = threading.Thread(target=receive_message, args=(client_socket,), daemon=True)
receive_thread.start()

send_message(client_socket)