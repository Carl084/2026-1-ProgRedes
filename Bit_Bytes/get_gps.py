import struct

'''O bloco EXIF sempre começa com a assinatura Exif seguida de dois bytes nulos: Exif\x00\x00'''
def get_gps(exif_bytes):
    if exif_bytes[:6] != b'Exif\x00\x00':
        return None #Os primeiros 6 bytes não for o EXIF. return ocorrera evitando ler algo corrompido ou formato diferente

    tiff = exif_bytes[6:] #Pula os 6 bytes do cabeçalho
    endian = '>' if tiff[:2] == b'MM' else '<' #O TIFF começa com 2 bytes indicando a ordem dos bytes
    ifd0_offset = struct.unpack(endian + 'I', tiff[4:8])[0] #Os bytes 4–8 do TIFF contêm o offset

    def read_ifd(offset):
        count = struct.unpack(endian + 'H', tiff[offset:offset+2])[0] #Os 2 bytes do IFD indicam quantas entradas existem
        '''Percorre as count e monta um dicionário. Pula 2 bytes do count, e i*12 avança entrada por entrada.'''
        return {
            struct.unpack(endian + 'H', tiff[offset+2+i*12:offset+2+i*12+2])[0]:
            tiff[offset+2+i*12+8:offset+2+i*12+12]
            for i in range(count)
        }

    ifd0 = read_ifd(ifd0_offset)
    #A tag 0x8825 é onde tem o GPS. Se não existir, a foto não tem GPS
    if 0x8825 not in ifd0:
        return None
    
    #ifd0[0x8825] retorna os 4 bytes do value_raw da tag GPS, que é um offset apontando para o GPS IFD
    #struct.unpack converte esses bytes para inteiro, e read_ifd lê o GPS IFD nessa posição
    gps = read_ifd(struct.unpack(endian + 'I', ifd0[0x8825])[0])
    if not all(k in gps for k in [1, 2, 3, 4]): #Verifica se as 4 tags necessárias existem no GPS IFD:
        return None                             #1 = GPSLatitudeRef   (N ou S)
                                                #2 = GPSLatitude      (graus, minutos, segundos)
                                                #3 = GPSLongitudeRef  (E ou W)
                                                #4 = GPSLongitude     (graus, minutos, segundos)

    def to_deg(value_raw):
        '''O value_raw é um offset apontando para onde estão os 3 racionais (graus, minutos, segundos) no TIFF'''
        off = struct.unpack(endian + 'I', value_raw)[0]
        #Cada racional ocupa 8 bytes, 4 de numerador e 4 de denominador
        vals = [struct.unpack(endian + 'I', tiff[off+i*8:off+i*8+4])[0] / #Lê os 3 racionais e divide numerador/denominador
                struct.unpack(endian + 'I', tiff[off+i*8+4:off+i*8+8])[0]
                for i in range(3)]
        
        return vals[0] + vals[1]/60 + vals[2]/3600 #Converte para grau decimal

    '''to_deg(gps[2]) converte a latitude para grau decimal. Depois verifica o LatitudeRef (tag 1) para saber o sinal.
        gps[1] é o value_raw da tag LatitudeRef. O struct.unpack converte para inteiro, e lê 1 byte nessa posição que 
        será b'N' ou b'S'''
    lat = to_deg(gps[2]) * (-1 if tiff[struct.unpack(endian+'I',gps[1])[0]:struct.unpack(endian+'I',gps[1])[0]+1] == b'S' else 1)
    
    # O mesmo se aplica a lon, sendo que esse 1 byte sera b'L' ou b'W'
    lon = to_deg(gps[4]) * (-1 if tiff[struct.unpack(endian+'I',gps[3])[0]:struct.unpack(endian+'I',gps[3])[0]+1] == b'W' else 1)

    return lat, lon