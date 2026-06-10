import socket

HOST = "httpbin.org"
PORT = 80


request = (
    f"GET /get HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "Transfer-encoding: chunked\r\n"
    "Connection: close\r\n"
    "\r\n"
)

sock = socket.socket(
    socket.AF_INET, 
    socket.SOCK_STREAM
    )
sock.connect((HOST, PORT))
sock.sendall(request.encode())

with open("x.txt", "wb") as arq:   
    while True:
        data = sock.recv(4096)
        
        if not data:
            break
        
        arq.write(data)

sock.close()