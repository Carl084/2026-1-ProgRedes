import socket

HOST = "viacap.com.br"
PORT = 80
PATH = "viacap.com.br/ws/RN/Natal/morais/json/"

request = (
    f"GET {PATH} HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Connection: close\r\n"
    "\r\n"
)
    #"Transfer-encoding: chunked\r\n"

sock = socket.socket(
    socket.AF_INET, 
    socket.SOCK_STREAM
    )
sock.connect((HOST, PORT))
sock.sendall(request.encode())

with open("x.json", "wb") as arq:   
    while True:
        data = sock.recv(4096)
        
        if not data:
            break
        
        arq.write(data)

sock.close()