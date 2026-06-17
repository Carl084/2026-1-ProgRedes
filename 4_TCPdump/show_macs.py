from datetime import datetime

nome_arquivo = input("Nome do arquivo: ")


fd = open(nome_arquivo, "rb")
cab_arq = fd.read(24)
magic = int.from_bytes(cab_arq[:4], 'big')
if magic in (0xA1B2C3D4, 0xA1B23C4D):
   endian = 'big'
else:
   endian = 'little'

if magic == 0xA1B2C3D4:
    tempo_adic = "us"
else:
    tempo_adic = "ns"

qtde_pacotes = 0
cab_pacote = fd.read(16)
MACs = set()

while cab_pacote != b'':
    qtde_pacotes += 1
    tempo_s  = int.from_bytes(cab_pacote[:4], endian)
    tempo_txt = datetime.utcfromtimestamp(tempo_s)
    tempo_extra = int.from_bytes(cab_pacote[4:8], endian)
    # input (f"{tempo_txt}.{tempo_extra}{tempo_adic}")
    
    tam_pac  = int.from_bytes(cab_pacote[8:12], endian)
    tam_orig = cab_pacote[12:16]
    
    pacote = fd.read(tam_pac)
    MACs.add(pacote[0:6])
    MACs.add(pacote[6:12])

    cab_pacote = fd.read(16)
print (f"#pacotes: {qtde_pacotes}")

MACs = [':'.join([f"{x:02x}" for x in MAC]) for MAC in MACs]

print (f"MACs: {MACs}")
fd.close()