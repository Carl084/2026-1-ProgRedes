import socket

SERVER_FILES="../server_files/"
SERVER_IP = "0.0.0.0"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, 12345))

print("IP em uso:",SERVER_IP)
print (f"[!] pronto para atender pedidos")

while True:
    # Le do cliente o nome do arquivo
    file_name, source = sock.recv(512)
    fd = open (SERVER_FILES+file_name.decode(), "rb")

    # indo para o final do arquivo
    pos_final = fd.seek(0, 2) 
    tamanho = pos_final.to_bytes(4, 'big')
    sock.sendall(tamanho, source)

    # voltando para o inicio do arquivo
    fd.seek(0, 0)
    data = fd.read(16384)
    total = 0
    while data != b"":
        print ("[?] enviando dados ...")
        sock.sendall(data, source)
        total += len(data)
        print (f"[!] total de bytes enviados: {total}")

        data = fd.read(16384)
    print (f"[!] arquivo enviado completamente")
    fd.close()