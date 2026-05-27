import socket
from introducao_socket.echo_config import *

def get_my_ip10():
    return (addr[4][0]
            for addr in socket.getaddrinfo(socket.get)
                if addr[4][0].startwith)

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_ip = socket.gethostbyname(socket.gethostname())
print(f"Conectado a {my_ip}:{SERVER_PORT}")

my_sock.bind((my_ip, SERVER_PORT))

while True:
    
    msg, source = my_sock.recvfrom(512)
    my_sock.sendto(msg, source)
    
    '''read = msg.decode()
    if read == "stop":
        break'''
                
my_sock.close()