def cifra(bloco, chave):
    ind_chave = 0
    for pos in range(bloco):
        bloco[pos] = ord(bloco[pos])^ord(chave[ind_chave])
    ind_chave += 1
    if ind_chave == len(chave):
        ind_chave = 0
        
