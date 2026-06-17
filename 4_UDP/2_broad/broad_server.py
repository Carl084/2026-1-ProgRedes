import socket
from config import *

def get_my_ip10():
    return [addr[4][0] 
         for addr in socket.getaddrinfo(socket.gethostname(), 80) 
             if addr[4][0].startswith('10.')
        ][0]

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_ip = get_my_ip10()
users = set()

print (f"Escutando em ({my_ip}:{PORT})")
my_sock.bind ((my_ip, PORT))

msg = b''
while msg != END:
    msg, source = my_sock.recvfrom(512)
    users.update([source])
    for user in users:
        if user != source:
            my_sock.sendto(msg, user)
            
print (f"Recebi {END}. Saindo.")
my_sock.close()