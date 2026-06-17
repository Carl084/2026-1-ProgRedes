import socket
from config import *

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_sock.settimeout(1)

server_ip = input ("IP/nome do servidor: ")

msg = b''
while msg != END:
    msg = input("Mensagem: ").encode()
    if msg:
        print (f"Enviando: {msg}")
        my_sock.sendto(msg, (server_ip, PORT))
    try:
        answer, source = my_sock.recvfrom(512)
        print (f"Recebido de {source}: {answer}")
    except socket.timeout as e:
        print (f"Sem mensagem a receber")
        None
print (f"Digitado {END}. Saindo.")
my_sock.close()