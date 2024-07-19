import subprocess
import webbrowser
import hashlib
import base58
import os
import re
import sys
import time



def busca_configuracoes():
    with open('configuracoeskeyhunt.txt', 'r') as config:
        linhas = config.readlines()
    
    range_inicial = linhas[0].strip()
    range_final = linhas[1].strip()
    k = int(linhas[2].strip())
    threads = int(linhas[3].strip())
    argS = linhas[4].strip()
    argR = linhas[5].strip()
    if argS == "None":
        argS = ''
    if argR == "None":
        argR = ''
    return range_inicial, range_final, k, threads, argS, argR

def quebrar_chave(chave_publica, address):
    range_inicial, range_final, k, threads, argS, argR = busca_configuracoes()
    with open ('in.txt', 'w') as save:
        save.write(chave_publica)
        time.sleep(1)
    script_keyhunt = f"./keyhunt -m bsgs -f in.txt -r {range_inicial}:{range_final} -k {k} -t {threads}{argS}{argR}"
    verificar = f'https://mempool.space/pt/address/{address}'
    webbrowser.open_new_tab(verificar)
    print(script_keyhunt)
    try:
        subprocess.run(script_keyhunt, shell=True, input=b'\n')
    
    except Exception as e:
        print(f"Erro ao executar iniciar o Keyhunt\nScript usado: {script_keyhunt}\n Erro: {e}")

def converter_wif(address, private_key_hex: str) -> str:
    private_key_hex.lower()
    # Remove o prefixo 0x se ele estiver presente
    if private_key_hex.startswith('0x'):
        private_key_hex = private_key_hex[2:]

    private_key_hex = private_key_hex.zfill(64)

    # Adiciona o prefixo 0x80 para a mainnet
    prefix = b'\x80'
    private_key_bytes = bytes.fromhex(private_key_hex)
    # Adiciona o sufixo 0x01 para indicar que é uma chave comprimida
    compressed_suffix = b'\x01'
    extended_key = prefix + private_key_bytes + compressed_suffix
    
    # Realiza o SHA-256 duplo do extended_key
    first_sha256 = hashlib.sha256(extended_key).digest()
    second_sha256 = hashlib.sha256(first_sha256).digest()
    
    # Adiciona os 4 primeiros bytes do segundo SHA-256 ao final do extended_key
    checksum = second_sha256[:4]
    final_key = extended_key + checksum
    
    # Converte para base58
    wif_compressed = base58.b58encode(final_key)
    with open('WIF.txt', 'a') as wif:
        wif.write(f'Endereço: {address}\n WIF: ' + wif_compressed.decode('utf-8') + '\n\n')
    
    return wif_compressed.decode('utf-8')

def aguarda_quebra(segundos:int): #Apos chamar o quebrar chave, fica procurando a key no arquivo Found.txt na raiz
    found = 'KEYFOUNDKEYFOUND.txt'
    time.sleep(1)
    for x in range(segundos):
        sys.stdout.write(f"\rEsperando Quebra da Chave... {x +1}... / {segundos}\n")
        sys.stdout.flush()
        if os.path.exists(found):
            with open(found, "r") as file:
                content = file.read()
                match = re.search(r'Private Key: (\w+)', content)
                if match:
                    return match.group(1)
        time.sleep(1)

    print('\nVerifique se houve erro, Arquivo não encontrado.')
    if input("Tentar novamente? (s/n): ").lower() in ['s', 'sim', 'y', 'yes']:
        x = int(input("Digite quantos segundos quer aguardar: "))
        aguarda_quebra(x)
    else:
        chave_privada = input("Insira a chave privada: ")
        return chave_privada

