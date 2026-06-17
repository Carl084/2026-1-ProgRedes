import socket
import sys

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

# Salvando o conteúdo em um arquivo
with open(archive, "wb") as file:
    file.write(body)
    
print(f"Dados do arquivo salvo em {archive} com sucesso!")