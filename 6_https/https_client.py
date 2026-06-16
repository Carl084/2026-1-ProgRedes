import sys
import socket
import ssl

B2NL = b"\r\n\r\n"
BNL  = b"\r\n"

def wrap_socket(sock, serverurl):
    purpose = ssl.Purpose.SERVER_AUTH
    context = ssl.create_default_context(purpose)
    return context.wrap_socket(sock, server_hostname=serverurl)

def get_block(data, block_len):
    while len(data) < block_len:    
        data += my_sock.recv(4096)
    return data[:block_len], data[block_len:]

def read_until(data, end):
    while end not in data:
        data += my_sock.recv(4096)
    return data

def get_chunk(data):
    data = read_until(BNL)
    posNL = data.find(BNL)
    len_chunk = int(data[:posNL], 16)
    
    chunk, data = get_block(data[posNL+2:], len_chunk)
    data = read_until(data, BNL)
    data = data[2:]
    return chunk, data

def get_data(host, port, resource, output):
    my_sock.connect((host, port))

    my_sock.send (("GET "+resource+" HTTP/1.1\r\n"+
                   "Host: "+host+"\r\n"+
                   "\r\n").encode())


    data = my_sock.recv(4096)
    data = read_until(data, B2NL)
    
    pos2NL = data.find(B2NL)
    headers = data[:pos2NL].decode().upper().split('\r\n')

    len_data = -1
    chunked = False
    for header in headers[1:]:
        header = header.split(": ")
        if header[0] == "CONTENT-LENGTH":
            len_data = int(header[1])
        if (header[0] == "TRANSFER-ENCODING" and
            header[1] == "CHUNKED"):
            chunked = True

    data = data[pos2NL+4:]
    if len_data != -1:
        print (f"Tamanho dos dados: {len_data}")
        only_data, _ = get_block(data, len_data)
    elif chunked:
        print (f"Transferencia em blocos!")
        only_data = b''
        chunk, data = get_chunk(data)
        while len(chunk) > 0:
            only_data += chunk
            chunk, data = get_chunk(data)

    if (len_data != -1) or chunked: 
        fd = open(output, "wb")
        fd.write(only_data)
        fd.close()
        print (f"Arquivo salvo em {output}")
    else:
        print ("Formato de transferencia nao identificado.")


my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) == 4:
    host = sys.argv[1]
    if host.lower().startswith("https://"):
        host = host[8:]
        port = 443
        my_sock = wrap_socket(my_sock, host)
    else:
        port = 80

    get_data(host, port, sys.argv[2], sys.argv[3])
else:
    print (f"uso: python {sys.argv[0]} site resource output_filename")
    print ("Exemplos:")
    print (f" python {sys.argv[0]} httpbin.org /image/png porco.png")
    print (f" python {sys.argv[0]} viacep.com.br /ws/59062570/json/ meucep.json")
    print (f" python {sys.argv[0]} httpbin.org /image/jpeg lobo.jpg")
my_sock.close()