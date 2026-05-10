import os, struct, webbrowser

'''Identificar as imagens JPEG'''
def search_jpegs(dirctory):
    photos = [f for f in os.listdir(dirctory) if f.lower().endswith((".jpg", ".jpeg"))]
    
    if not photos:
        exit("Nenhuma imagem JPEG encontrada.")
        
    else:
        return photos

'''Coletar os dados EXIF em bytes'''
def extract_exif(path):
    with open(path, "rb") as f:
        data = f.read()

    if data[:2] != b'\xFF\xD8':
        print("Não é JPEG válido")
        return None

    i = 2
    while i < len(data) - 4:
        if data[i] != 0xFF:
            break

        marker = data[i:i+2]
        size = struct.unpack(">H", data[i+2:i+4])[0]

        if marker == b'\xFF\xE1':
            return data[i+4:i+2+size]

        i += 2 + size

    return None

'''Ler o IFD e montar o dicionario das entradas'''
def read_ifd(offset):
    count = struct.unpack(endian + 'H', tiff[offset:offset+2])[0]
    return {
        struct.unpack(endian + 'H', tiff[offset+2+i*12:offset+2+i*12+2])[0]:
        tiff[offset+2+i*12+8:offset+2+i*12+12]
        for i in range(count)
    }

'''Conversor para grau decimal'''
def to_deg(value_raw):
    off = struct.unpack(endian + 'I', value_raw)[0]
    vals = [struct.unpack(endian + 'I', tiff[off+i*8:off+i*8+4])[0] /
            struct.unpack(endian + 'I', tiff[off+i*8+4:off+i*8+8])[0]
            for i in range(3)]
    
    return vals[0] + vals[1]/60 + vals[2]/3600


'''Receber o diretorio das imagens'''

path = input("Digite o caminho :").strip().strip('"')

if not path:
    exit("Caminho não encontrado.")
    
else:
    try:
        dirctory = os.path.abspath(path)
        photos = search_jpegs(dirctory)
        
        coords = []
        
        for f in photos[:10]:
            filepath = os.path.join(dirctory, f)
            exif_bytes = extract_exif(filepath)
            
            if not exif_bytes:
                print(f"{f}: sem EXIF")
                continue
                
            tiff = exif_bytes[6:]
            endian = '>' if tiff[:2] == b'MM' else '<'
            ifd0_offset = struct.unpack(endian + 'I', tiff[4:8])[0]
                
            ifd0 = read_ifd(ifd0_offset)
            if 0x8825 not in ifd0:
                print(f"A foto: {f}, não tem GPS.")
                continue
                    
                
            gps = read_ifd(struct.unpack(endian + 'I', ifd0[0x8825])[0])
            if not all(k in gps for k in [1, 2, 3, 4]):
                print("Há uma falta em uma das 4 tags do GPS")
            
            lat_ref = gps[1][0:1].decode('ascii')
            lon_ref = gps[3][0:1].decode('ascii')
            
            lat = to_deg(gps[2]) * (-1 if lat_ref == 'S' else 1)
            lon = to_deg(gps[4]) * (-1 if lon_ref == 'W' else 1)
            
            print(f"Coordenadas da imagem {f}: ( {lat}, {lon} )")
            
            coords.append((lat, lon))
        
        waypoints = "/".join(f"{lat},{lon}" for lat, lon in coords)
        url = f"https://www.google.com/maps/dir/{waypoints}"
        
        webbrowser.open(url)
        
    except Exception as e:
        print(f"Erro: {e}")