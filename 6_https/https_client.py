import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 4:
    print("Uso:")
    print(f"python {sys.argv[0]} site recurso arquivo")
    sys.exit()

site = sys.argv[1]
recurso = sys.argv[2]
arquivo = sys.argv[3]

sock.connect((site, 80))

# Montando a requisição HTTP
request = (
    f"GET {recurso} HTTP/1.1\r\n"
    f"Host: {site}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

sock.send(request.encode())

# Recebendo os dados
dados = b""

while True:

    parte = sock.recv(4096)

    if len(parte) == 0:
        break

    dados += parte

sock.close()

# Procurando o fim do cabeçalho
posicao = dados.find(b"\r\n\r\n")

cabecalho = dados[:posicao].decode()
corpo = dados[posicao + 4:]

print("Cabeçalho recebido:")
print(cabecalho)

# Salvando o conteúdo em arquivo
arq = open(arquivo, "wb")
arq.write(corpo)
arq.close()

print("Arquivo salvo com sucesso!")