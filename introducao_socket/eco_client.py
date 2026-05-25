import socket
from config import *

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_ip = input("IP/nome do servidor: ")

while True:
    msg = input("Mensagem: ")
    
    if not msg:
        break
    
    print(f"Enviando: {msg}")
    
    my_sock.sendto(msg.encode(), (server_ip, PORT))
    
    answer, source = my_sock.recvfrom(512)
    
    print(f"Recebido de {source}: {answer.decode()}")
    
my_sock.close()