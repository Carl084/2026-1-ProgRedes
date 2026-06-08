import socket, threading

def get_my_ip10():
    # Andar sobre os endereços da maquina
    for addr in socket.getaddrinfo(socket.gethostname(), None): 
        ip = addr[4][0] # Extrair o IP
        
        if ip.startswith("10."): # verificar se começa com 10
            return f"{ip}" # Retorna ele
    
    return None # Caso não tenha 10

HOST_IP = get_my_ip10
print(f"O IP:{HOST_IP}")
PORT = input("Número da porta: ")

clients = []

def trat_pacote():
    
    return

def broadcast(msg, remate=None):
    for client in clients:
        if client != remate:
            try:
                client.send(msg)
            except:
                client.remove(client)
                client.close()

def acp_client(client, address):
    print(f"[NOVA CONEXÃO] {address}")
    
    while True:
        try:
            cabecalho = client.recv(1024).decode()
            
            partes = cabecalho.split("|")
            
            if tipo == "MSG":
                trat_pacote()
                
            elif tipo == "FILE":
                
            
            if not dados:
                break
            
            msg = dados.decode()
            print(f"{address}: {dados.decode()}")
            
            broadcast(
                f"{address}: {msg}".encode(),
                client
            )
            
        except:
            break
        
        print(f"[DESCONECTADO] {address}")
        
        clients.remove(client)
        client.close()

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST_IP, PORT))
server.listen()

print(f"Server Iniciado!")

while True:
    
    client, address = server.accept()

    thread = threading.Thread(
        target=acp_client,
        args=(client, address)
    )
    
    thread.start()
    
    print(f"Clientes ativos: {threading.active_count() - 1}")

cabecalho = client.recv(1024).decode()
partes = cabecalho.split("|")
tipo = partes[0]

if tipo == "MSG":
    msg = partes[1]
    print(f"Mensagem recebida: {msg}")

elif tipo == "FILE":
    name_arq = partes[1]
    size = int(partes[2])
    
    print(f"Recebendo arquivo {name_arq}")

server.close()