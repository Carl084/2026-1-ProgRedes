import socket
from echo_config import *

def get_my_ip10():
    # Andar sobre os endereços da maquina
    for addr in socket.getaddrinfo(socket.gethostname(), None): 
        ip = addr[4][0] # Extrair o IP
        
        if ip.startswith("10."): # verificar se começa com 10
            return ip # Retorna ele
    
    return None # Caso não tenha 10

my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_ip = get_my_ip10()

print(f"Server iniciado em {my_ip}:{SERVER_PORT}")
my_sock.bind((my_ip, SERVER_PORT))

while True:
    msg, source = my_sock.recvfrom(512)
    print(f"Recebido de {source}: {msg.decode()}")
    
    clients.add(source) # Adicionar client a lista
    print(f"Clientes conectados: {clients}")
    
    # Enviar mensagem para todos menos para a origem
    for client in clients:
        if client != source: # se não for a origem, enviar mensagem
            print(f"Enviando para {client}")
            my_sock.sendto(msg, client)
            
my_sock.close()