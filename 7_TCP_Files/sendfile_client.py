import socket

CLIENT_FILES="../client_files/"
SERVER_IP = input("Digite o IP do servidor a conectar")
SERVER = (SERVER_IP, 12345)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    file_name = input("Nome do arquivo a baixar: ")
    sock.sendall(file_name.encode(), SERVER)

    fd = open (CLIENT_FILES+file_name, "wb")

    print ("[?] esperando tamanho ...")
    tamanho, source  = sock.recv(4)
    tamanho = int.from_bytes(tamanho, 'big')

    print ("[?] esperando dados ...")
    data, source = sock.recv(16384)
    total = len(data)

    while total < tamanho:
        print (f"[!] total de bytes lidos: {total}")
        fd.write(data)

        print ("[?] esperando dados ...")
        data, source = sock.recvfrom(16384)
        total += len(data)
    fd.close()