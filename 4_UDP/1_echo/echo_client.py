import socket, os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

PORT = 12345
END = b'FIM'

server_ip = input ("IP/nome do servidor: ")

msg = b''
while msg != END:
    msg = input("Mensagem: ").encode()
    if msg:
        print (f"Enviando: {msg}")
        sock.sendto(msg, (server_ip, PORT))
        answer, source = sock.recvfrom(512)
        print (f"Recebido de {source}: {answer}")

print (f"Digitado {END}. Saindo.")
sock.close()