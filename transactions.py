from bit import PrivateKey, network
from time import sleep
import sys
import requests

def transferir(wif, destino):
    if destino == 'Não Informado':
        print('\nTransferencia não informada, endereço não informado.\n')
        return None
    my_key = PrivateKey(wif)
    print('Endereço da Carteira Capturada: ', my_key.address)
    saldo = my_key.balance_as('satoshi')
    print('Saldo da Carteira Capturada: ', saldo)
    taxa = network.get_fee('fast') 
    print(f'Taxa de Transação Sugerida (satoshis por byte): {taxa}')
    taxa *= 2
    taxa = int(taxa)
    print(f'Taxa a ser utilizada: ', taxa)
    valor = int(saldo)-taxa
    valor = int(valor)
    if valor < 0:
        print(f'-\n-----------------\nSaldo nao possibilita transação: {saldo} satoshis\n ------------------')
        return None
    print(f'Valor a ser transferido: {valor} satoshis')
    print ('Iniciando a transferencia...')
    try:
        tx_hash = my_key.send([(destino, valor, "satoshi")], fee=taxa)
        if tx_hash:
            print('\n\nTransação Enviada com Sucesso !!!! ---- \n--- Hash da transação: ',tx_hash, '\n---')
            return tx_hash
        else:
            print('\n---------------Falha ao transferir, tente manualmente.---------------')
            return None
    except:
        print('\n---------------Falha ao transferir, tente manualmente.---------------')
        return None
    
def verifica_saldo(endereco):
    for x in range(50):
        sys.stdout.write(f"\rVerificando Saldo da Carteira... Tentativa {x +1}... / 50 ")
        sys.stdout.flush()
        transacoes = network.NetworkAPI.get_transactions(address=endereco)
        saldo = network.NetworkAPI.get_balance(endereco) / 1e8
        
        if saldo > 0:
            print(f"\n---------------Valor recebido com sucesso: {saldo:.8f} BTC---------------")
            return
        
        if transacoes:
            print(f'\nExiste Transferencia, saldo atual: {saldo:.8f} BTC\nID: {transacoes}')
        else:
            print(f'\nNão existe transações em andamento, saldo atual: {saldo:.8f} BTC')

        sleep(5)

def monitorar_mempool(address):
    while True:
        try:
            url = f'https://blockchain.info/rawaddr/{address}'
            response = requests.get(url)
            print(f'Procurando Chave Pública... Chamando API... Resposta API: {response}')
            if response.status_code == 200:
                data = response.json()
                transactions = data.get('txs', [])
            if transactions:
                for tx in transactions:
                    for input_tx in tx.get('inputs', []):
                        if input_tx.get('prev_out', {}).get('addr') == address:
                            script = input_tx.get('script')
                            if script != '':
                                script = script[-66:]
                                with open('PublicKey.txt', 'a') as pk:
                                    pk.write(f'Endereço: {address} \nChave Pública: {script}\n\n')
                                return script

            print('Não encontrada chave publica, tentando novamente em 5 segundos\n Procurando...\nAo encontrar uma página será aberta para conferencia da chave pública...')
            sleep(5)
        except Exception as e:
            print (f"Ocorreu uma Excessão ao chamar a API\nSe ocorrer varias vezes verifique se o endereço fornecido está correto\nTentando novamente em 5 segundos")
            sleep(5)


