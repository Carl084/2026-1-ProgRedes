import socket, threading

''' 
    def get_my_ip10():
        # Andar sobre os endereços da maquina
        for addr in socket.getaddrinfo(socket.gethostname(), None): 
            ip = addr[4][0] # Extrair o IP
        
            if ip.startswith("10."): # verificar se começa com 10
                return f"{ip}" # Retorna ele
    
        return None # Caso não tenha 10
'''

HOST = "0.0.0.0"
PORT = 5000

clients = []


def broadcast(msg, remate=None): # Definir ação broadcast.
    for client in clients[:]:
        if client != remate: 
            try:
                client.send(msg)
            except:
                client.remove(client)
                client.close()


def to_receive_arq(client, name_arq, size): # Recebendo o arquivo.
    received = 0

    # Ler toda a mensagem e grava-lo em um outro arquivo.
    with open(f"recebido_{name_arq}", "wb") as arq: 

        while received < size:

            data = client.recv(
                min(4096, size - received)
            )

            if not data:
                break

            arq.write(data)
            received += len(data)

    print(f"Arquivo recebido: {name_arq}")


def to_attend_client(client, address):

    print(f"[NOVA CONEXÃO] {address}")

    while True:

        try:
            header = client.recv(1024)

            if not header:
                break
            
            header = header.decode()
            parts = header.split("|")
            t_type = parts[0]

            if t_type == "MSG":
                
                msg = parts[1]
                print(f"{address}: {msg}")

                broadcast(
                    f"{address}: {msg}".decode(),
                )

            if t_type == "FILE":

                name_arq = parts[1]
                size = int(parts[2])

                print(
                    f"{address} enviou um arquivo "
                    f"{name_arq} ({size} bytes)"
                )

                client.send(b"OK")

                to_receive_arq(
                    client,
                    name_arq,
                    size
                )

        except Exception as erro:

            print(f"Erro: {erro}")
            break

    print(f"[DESCONECTADO] {address}")

    if client in clients:
        client.remove(client)
    
    client.close()

server = socket.socket(
    socket.AF_INET
    socket.SOCK_STREAM
)

server.bind((HOST, PORT))
server.listen()

print(f"Servidor ouvido em {HOST}:{PORT}")

while True:

    client, address = server.accept()
    clients.append(client)

    thread = threading