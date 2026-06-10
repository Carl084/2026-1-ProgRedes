import socket, os

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST_IP = input("IP/nome do servidor: ")
PORT = int(input("Número da porta: "))

sock.connect((HOST_IP, PORT))

def env_msg():
    msg = input("Mensagem: ")
    
    if not msg:
        return
    
    dados = f"MSG|{msg}"
    
    print(f"Enviando: {msg}")
    sock.send(msg.encode()) # Mensagem enviada
    
def env_arq():
    file = input("caminho do arquivo: ")
    name = os.path.basename(file)
    size = os.path.getsize(file)
    
    cabecalho = f"FILE|{name}|{size}"
    sock.send(cabecalho.encode())
    
    sock.recv(1024)
    
    with open(file, "rb") as f:
        while True:
            dados = f.read(4096)
            
            if not dados:
                break
            
            sock.sendall(dados)
    
    print("Arquivo enviado")
    

def hub():
    while True:
        print("Opções")
        print("MSG: Enviar Mensagens")
        print("FILE: Enviar Arquivo")
        op = input("Sua escolha: ")
        
        if op == "MSG":
            env_msg()
        elif op == "FILE":
            env_arq()


sock.close()