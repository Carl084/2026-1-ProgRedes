from datetime import datetime

nome_arquivo = input("Nome do arquivo: ")


fd = open(nome_arquivo, "rb")
cab_arq = fd.read(24)
magic = int.from_bytes(cab_arq[:4], 'big')
if magic in (0xA1B2C3D4, 0xA1B23C4D):
   endian = 'big'
else:
   endian = 'little'

print (hex(magic))
if magic == 0xA1B2C3D4:
    tempo_adic = "us"
else:
    tempo_adic = "ns"

cab_pacote = fd.read(16)
while cab_pacote != b'':
    tempo_s  = int.from_bytes(cab_pacote[:4], endian)
    tempo_txt = datetime.utcfromtimestamp(tempo_s)
    tempo_extra = int.from_bytes(cab_pacote[4:8], endian)
    input (f"{tempo_txt}.{tempo_extra}{tempo_adic}")
    
    tam_pac  = int.from_bytes(cab_pacote[8:12], endian)
    tam_orig = cab_pacote[12:16]
    
    fd.seek(tam_pac, 1)
    cab_pacote = fd.read(16)

fd.close()