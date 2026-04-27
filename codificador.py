import os, sys

nome_arquivo = input("Digite o nome do arquivo que quer cifrar: ")

try:
    with open(nome_arquivo, "rb") as arquivo:
        conteudo = arquivo.read()
except FileNotFoundError:
    print("Arquivo não existe!")

palavra_chave = input("digite a palavra: ")
if palavra_chave == "":
    print("Escreva uma palavra")
    
chave_byte = palavra_chave.encode("utf-8")
tamanho_chave = len(chave_byte)

