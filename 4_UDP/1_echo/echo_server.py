import socket

PORT = 12345
END = b'FIM'

def get_my_ip10():
    return [addr[4][0] 
         for addr in socket.getaddrinfo(socket.gethostname(), 80) 
             if addr[4][0].startswith('10.')
        ][0]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip = get_my_ip10()

print (f"Escutando em ({ip}:{PORT})")
sock.bind ((ip, PORT))

msg = b''
while msg != END:
    msg, source = sock.recvfrom(512)
    print (f"Recebi/devolvendo a {source}: {msg}")
    sock.sendto(msg, source)

print (f"Recebi {END}. Saindo.")
sock.close()