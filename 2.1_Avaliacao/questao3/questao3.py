# Coloque aqui o nome e matrícula do(s) componente(s) do grupo. 
# 20252014050006 - Carlos William Felix de Lima 
# 20252014050001 - Luidhy Anthony Lima Dos Anjos

import struct, os

def inicializaRAID():
    disk_quant = int(input("Digite a quantidade de discos: "))
    size_disk_mb = int(input("Digite o tamanho dos discos (MB): "))
    size_block_kb = int(input("Digite o tamanho do bloco (KB): "))

    size_disk = size_disk_mb * 1024 * 1024
    block_size = size_block_kb * 1024

    path = input("Digite o caminho para salvar os dados: ").strip().strip('"')

    if not path:
        exit("Caminho inválido.")

    os.makedirs(path, exist_ok=True)

    header_size = struct.calcsize("II")
    disk_body = b"\x00" * (size_disk - header_size)

    for disk_id in range(disk_quant):

        disk_name = f"disco{disk_id}.bin"
        disk_path = os.path.join(path, disk_name)

        header = struct.pack("II", disk_id, block_size)

        with open(disk_path, "wb") as disk_file:
            disk_file.write(header)
            disk_file.write(disk_body)

    print(f"\n{disk_quant} discos criados com sucesso.")

def obtemRAID():

    disk_quant = int(input("Digite a quantidade de discos: "))
    size_disk_mb = int(input("Digite o tamanho dos discos (MB): "))
    size_block_kb = int(input("Digite o tamanho do bloco (KB): "))

    size_disk = size_disk_mb * 1024 * 1024
    block_size = size_block_kb * 1024

    path = input("Digite o caminho dos discos: ").strip().strip('"')

    if not path:
        exit("Caminho não encontrado.")

    discos = []
    ausentes = []

    for disk_id in range(disk_quant):

        disk_path = os.path.join(path, f"disco{disk_id}.bin")

        if os.path.exists(disk_path):
            discos.append(disk_path)
        else:
            discos.append(None)
            ausentes.append(disk_id)

    if len(ausentes) > 1:

        print("Impossível operar. Mais de um disco ausente:\n")

        for disk_id in ausentes:
            print(f"  disco{disk_id}.bin não encontrado")

        exit()

    if len(ausentes) == 1:
        print(f"\nAviso: disco{ausentes[0]}.bin não encontrado (modo degradado).")

    raid = {
        "discos": discos,
        "disk_quant": disk_quant,
        "size_disk": size_disk,
        "block": block_size,
        "path": path,
        "ausente": ausentes[0] if ausentes else None
    }

    return raid

def reconstroiRAID(raid):

    if raid["ausente"] is None:
        print("Nenhum disco ausente. Não é necessário reconstruir.")
        return

    missing_disk = raid["ausente"]
    header_size = struct.calcsize("II")

    dados = []

    # Lê os discos restantes
    for disk_id in range(raid["disk_quant"]):

        if disk_id == missing_disk:
            continue

        disk_path = raid["discos"][disk_id]

        with open(disk_path, "rb") as disk_file:

            disk_file.read(header_size)
            dados.append(disk_file.read())

    # Reconstrução usando XOR
    reconstruido = bytearray(dados[0])

    for data in dados[1:]:

        for i in range(len(reconstruido)):
            reconstruido[i] ^= data[i]

    # Cria novamente o disco ausente
    disk_path = os.path.join(
        raid["path"],
        f"disco{missing_disk}.bin"
    )

    header = struct.pack(
        "II",
        missing_disk,
        raid["block"]
    )

    with open(disk_path, "wb") as disk_file:

        disk_file.write(header)
        disk_file.write(reconstruido)

    raid["discos"][missing_disk] = disk_path
    raid["ausente"] = None

    print(f"disco{missing_disk}.bin reconstruído com sucesso!")

def escreveRAID(raid):

    num_data_disks = raid["disk_quant"] - 1

    header_size = struct.calcsize("II")
    disk_body_size = raid["size_disk"] - header_size

    logical_size = num_data_disks * disk_body_size

    data = input("Digite os dados a gravar: ").encode()

    position = int(
        input(f"Posição inicial (0 a {logical_size - 1}): ")
    )

    # Validações
    if position < 0 or position >= logical_size:
        print("Posição inválida!")
        return

    if position + len(data) > logical_size:
        print("Dados grandes demais para essa posição!")
        return

    # Escrita dos dados
    for offset, byte in enumerate(data):

        current_position = position + offset

        logical_block = current_position // raid["block"]
        block_offset = current_position % raid["block"]

        disk_index = logical_block % num_data_disks
        block_in_disk = logical_block // num_data_disks

        disk_position = (
            block_in_disk * raid["block"]
        ) + block_offset

        disk_path = raid["discos"][disk_index]

        if disk_path is None:
            continue

        with open(disk_path, "r+b") as disk_file:

            disk_file.seek(header_size + disk_position)
            disk_file.write(bytes([byte]))

    # Leitura dos discos para calcular paridade
    contents = []

    for disk_index in range(num_data_disks):

        disk_path = raid["discos"][disk_index]

        if disk_path is None:
            contents.append(bytearray(disk_body_size))
            continue

        with open(disk_path, "rb") as disk_file:

            disk_file.seek(header_size)
            contents.append(bytearray(disk_file.read()))

    # Calcula XOR da paridade
    parity = bytearray(contents[0])

    for content in contents[1:]:

        for i in range(len(parity)):
            parity[i] ^= content[i]

    # Escreve disco de paridade
    parity_disk = raid["discos"][raid["disk_quant"] - 1]

    with open(parity_disk, "r+b") as disk_file:

        disk_file.seek(header_size)
        disk_file.write(parity)

    print(f"{len(data)} byte(s) gravado(s) com sucesso!")

def leRAID(raid):

    num_data_disks = raid["disk_quant"] - 1

    header_size = struct.calcsize("II")
    disk_body_size = raid["size_disk"] - header_size

    logical_size = num_data_disks * disk_body_size

    position = int(
        input(f"Posição inicial (0 a {logical_size - 1}): ")
    )

    quantity = int(input("Quantos bytes ler: "))

    # Validações
    if position < 0 or position >= logical_size:
        print("Posição inválida!")
        return

    if position + quantity > logical_size:
        print("Quantidade excede o tamanho do RAID!")
        return

    result = bytearray()

    for offset in range(quantity):

        current_position = position + offset

        logical_block = current_position // raid["block"]
        block_offset = current_position % raid["block"]

        disk_index = logical_block % num_data_disks
        block_in_disk = logical_block // num_data_disks

        disk_position = (
            block_in_disk * raid["block"]
        ) + block_offset

        disk_path = raid["discos"][disk_index]

        # Disco disponível
        if disk_path is not None:

            with open(disk_path, "rb") as disk_file:

                disk_file.seek(header_size + disk_position)

                byte = disk_file.read(1)

                if byte:
                    result.append(byte[0])
                else:
                    result.append(0)

            continue

        # Reconstrução do byte usando XOR
        recovered_byte = 0

        for i in range(raid["disk_quant"]):

            if i == disk_index:
                continue

            other_disk = raid["discos"][i]

            if other_disk is None:
                continue

            with open(other_disk, "rb") as disk_file:

                disk_file.seek(header_size + disk_position)

                byte = disk_file.read(1)

                if byte:
                    recovered_byte ^= byte[0]

        result.append(recovered_byte)

    print(f"\nDados: {result.decode(errors='replace')}")
    print(f"Hex: {result.hex()}")

def removeDiscoRAID(raid):

    # Verifica se já existe disco ausente
    if raid["ausente"] is not None:

        print(
            f"Já existe um disco ausente "
            f"(disco{raid['ausente']}.bin). "
            f"Não é possível remover outro!"
        )

        return

    # Escolha do disco
    disk_index = int(
        input(
            f"Qual disco remover "
            f"(0 a {raid['disk_quant'] - 1})? "
        )
    )

    # Validação
    if disk_index < 0 or disk_index >= raid["disk_quant"]:

        print("Índice inválido!")
        return

    disk_path = raid["discos"][disk_index]

    # Segurança extra
    if disk_path is None or not os.path.exists(disk_path):

        print(f"disco{disk_index}.bin já está ausente!")
        return

    # Remove o disco
    os.remove(disk_path)

    # Atualiza estrutura RAID
    raid["discos"][disk_index] = None
    raid["ausente"] = disk_index

    print(
        f"disco{disk_index}.bin removido com sucesso.\n"
        f"Modo degradado ativado."
    )

def raid_carregado():

    if raid is None:
        print("Você precisa obter o RAID primeiro!")
        return False

    return True

# programa principal
raid = None

while True:

    print("\n########## MENU ##########")
    print("1. Inicializar RAID")
    print("2. Obter RAID")
    print("3. Reconstruir RAID")
    print("4. Escrever RAID")
    print("5. Ler RAID")
    print("6. Remover disco RAID")
    print("0. Sair")
    print("##########################")

    option = input("Sua opção: ").strip()

    match option:

        case "1":
            inicializaRAID()

        case "2":
            raid = obtemRAID()

        case "3":
            if raid_carregado():
                reconstroiRAID(raid)

        case "4":
            if raid_carregado():
                escreveRAID(raid)

        case "5":
            if raid_carregado():
                leRAID(raid)

        case "6":
            if raid_carregado():
                removeDiscoRAID(raid)

        case "0":
            print("Encerrando sistema RAID...")
            break

        case _:
            print("Opção inválida!")