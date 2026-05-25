import socket
from config import *

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

my_ip = socket.gethostbyname(socket.gethostname())
print(f"Conectado a {my_ip}:{PORT}")

my_sock.bind((my_ip, PORT))

while True:
    
    msg, source = my_sock.recvfrom(512)
    my_sock.sendto(msg, source)
    
    '''read = msg.decode()
    if read == "stop":
        break'''
                
my_sock.close()