# Coloque aqui o nome e matrícula do(s) componente(s) do grupo. 
# 20252014050006 - Carlos William Felix de Lima 
# 20252014050001 - Luidhy Anthony Lima Dos Anjos

import struct
import sys

def format_mac(dados):
    mac = ""
    for i in range(6):
        mac += "%02x" % dados[i]
        if i < 5: mac += ":"
    return mac

def format_ip(dados):
    return ".".join(map(str, dados))

def main():
    if len(sys.argv) < 2:
        print("uso: python script.py arquivo.pcap")
        return

    caminho = sys.argv[1]
    
    try:
        f = open(caminho, 'rb')
    except:
        print("erro ao abrir o arquivo")
        return

    g_header = f.read(24)
    if len(g_header) < 24:
        f.close()
        return

    magic = struct.unpack('I', g_header[:4])[0]
    ordem = '<' if magic == 0xd4c3b2a1 else '>'
    
    stats_vol = {}
    t_inicio = None
    t_fim = None

    while True:
        p_header = f.read(16)
        if not p_header:
            break
        
        sec, usec, c_len, _ = struct.unpack(f'{ordem}IIII', p_header)
        ts = sec + (usec / 1000000.0)
        
        if t_inicio is None: t_inicio = ts
        t_fim = ts

        raw = f.read(c_len)
        if len(raw) < 14: continue
        
        d_mac = format_mac(raw[0:6])
        s_mac = format_mac(raw[6:12])
        e_type = struct.unpack('!H', raw[12:14])[0]
        
        print("\n" + "-"*40)
        print("MAC Origem:", s_mac)
        print("MAC Destino:", d_mac)

        if e_type == 0x0800:
            ip_h = raw[14:34]
            ihl = (ip_h[0] & 0x0F) * 4
            proto = ip_h[9]
            ip_src = format_ip(ip_h[12:16])
            ip_dst = format_ip(ip_h[16:20])
            
            v_ttl = ip_h[8]
            v_id = struct.unpack('!H', ip_h[4:6])[0]
            v_flags = struct.unpack('!H', ip_h[6:8])[0]
            v_len = struct.unpack('!H', ip_h[2:4])[0]

            print(f"IP: {ip_src} -> {ip_dst}")
            print(f"Extras IP: TTL={v_ttl}, ID={v_id}, Flags={hex(v_flags)}, Tam={v_len}")

            stats_vol[ip_src] = stats_vol.get(ip_src, 0) + c_len
            stats_vol[ip_dst] = stats_vol.get(ip_dst, 0) + c_len

            l4 = raw[14 + ihl:]

            if proto == 1:
                tipo = l4[0]
                nomes = {0:"echo reply", 3:"unreachable", 5:"redirect", 8:"echo request", 11:"time exceeded"}
                print("Protocolo: ICMP (" + nomes.get(tipo, "outro") + ")")
                if tipo == 0 or tipo == 8:
                    i_id, i_seq = struct.unpack('!HH', l4[4:8])
                    print(f"  Info ICMP -> ID: {i_id}, Sequencia: {i_seq}")

            elif proto == 6:
                sp, dp, seq, ack, flg = struct.unpack('!HHIIH', l4[:14])
                win = struct.unpack('!H', l4[14:16])[0]
                print(f"Protocolo: TCP | Portas: {sp} -> {dp}")
                print(f"  Extras TCP -> Seq: {seq}, Ack: {ack}, Janela: {win}, Flags: {hex(flg & 0x1FF)}")

            elif proto == 17:
                sp, dp = struct.unpack('!HH', l4[:4])
                print(f"Protocolo: UDP | Portas: {sp} -> {dp}")

    f.close()

    print("\n" + "="*50)
    if stats_vol:
        vencedor = max(stats_vol, key=stats_vol.get)
        print("IP que mais trocou dados:", vencedor)
        print("Total de bytes:", stats_vol[vencedor])
    
    if t_inicio and t_fim:
        print("Duracao total da captura: %.4f segundos" % (t_fim - t_inicio))
        print("Intervalo: de", t_inicio, "ate", t_fim)

if __name__ == "__main__":
    main()
        
