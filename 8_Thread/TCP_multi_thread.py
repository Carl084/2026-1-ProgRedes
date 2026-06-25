import threading, socket

def client(conn):
    while True:
        dados = conn.recv(1024)

        if not dados:
            break

        conn.send(dados)
        
    conn.close()

server = socket.socket((
    socket.AF_INET,
    socket.SOCK_STREAM
    ))
server.bind(("0.0.0.0",5000))
server.listen()

# Cria-se um thread para cada cliente conectado.
while True:
    # accept bloquea até alguém conectar.
    conn, addr = server.accept()

    threading.Thread(
        target=client,
        args=(conn,)
    ).start()