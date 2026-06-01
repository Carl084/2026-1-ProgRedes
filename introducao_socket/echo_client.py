import socket
import threading
from echo_config import *

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

SERVER_IP = input("IP/nome do servidor: ")

def receber(): # Esperando mensagem
    while True:
        try:
            msg, source = my_sock.recvfrom(512)
            print(f"\n{source}: {msg.decode()}")
        except:
            break

threading.Thread(target=receber, daemon=True).start()

my_sock.sendto("ENTROU".encode(), (SERVER_IP, SERVER_PORT))

while True:
    msg = input("Mensagem: ")
    
    if not msg:
        break
    
    print(f"Enviando: {msg}")
    my_sock.sendto(msg.encode(), (SERVER_IP, SERVER_PORT)) # Mensagem enviada
    
my_sock.close()