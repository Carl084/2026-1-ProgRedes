# py https_client.py viacep.com.br /ws/59062570/json/ meucep.json
import socket
import sys

def decode_chunked(date):
    result = b""
    while date:
        pos = date.find(b"\r\n") # Encontrar a primeira quebra de linha
        if pos == -1:
            break

        size_hex = date[:pos] # Pega o Hex
        size = int(size_hex, 16) # Converter para decimal

        if size == 0:
            break

        start = pos + 2 # Onde realemte começa os dados
        end = start + size

        result += date[start:end]
        date = date[end+2:]

    return result

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 4:
    print("Uso:")
    print(f"python {sys.argv[0]} site recurso arquivo")
    sys.exit()

# Coletar as imformações do terminal
site = sys.argv[1]
resoucer = sys.argv[2]
archive = sys.argv[3]

sock.connect((site, 80))

# Requisição HTTP
request = (
    f"GET {resoucer} HTTP/1.1\r\n"
    f"Host: {site}\r\n"
    "Connection: close\r\n"
    "\r\n"
)

sock.send(request.encode())

date = b""

# Loop composto de ler os dados recebidos ate 4096 bytes e guardar em uma string
while True:

    part = sock.recv(4096)

    if len(part) == 0:
        break

    date += part

sock.close()

# Procurando o fim do cabeçalho
division = date.find(b"\r\n\r\n")
# Separar cabeça e corpo
header = date[:division].decode()
body = date[division + 4:]

print("Cabeçalho recebido:")
print(header)

body = decode_chunked(body).decode("utf-8")
# Salvando o conteúdo em um arquivo
with open(archive, "w", encoding="utf-8") as file:
    file.write(body)
    
print(f"Dados do arquivo salvo em {archive} com sucesso!")