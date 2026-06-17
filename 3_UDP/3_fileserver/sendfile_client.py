import socket

CLIENT_FILES="../client_files/"
SERVER = ("127.0.0.1", 12346)
my_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    file_name = input("Nome do arquivo a baixar: ")
    my_sock.sendto(file_name.encode(), SERVER)

    fd = open (CLIENT_FILES+file_name, "wb")

    print ("[?] esperando tamanho ...")
    tamanho, source  = my_sock.recvfrom(4)
    tamanho = int.from_bytes(tamanho, 'big')

    print ("[?] esperando dados ...")
    data, source = my_sock.recvfrom(16384)
    total = len(data)

    while total < tamanho:
        print (f"[!] total de bytes lidos: {total}")
        fd.write(data)

        print ("[?] esperando dados ...")
        data, source = my_sock.recvfrom(16384)
        total += len(data)
    fd.close()