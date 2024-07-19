from transactions import transferir, verifica_saldo, monitorar_mempool
from hashs import quebrar_chave, converter_wif, aguarda_quebra
from cleanup import limpeza, interrompido
import time
import signal
import atexit

sim = ['s', 'sim', 'y', 'yes']


def main(address, destino):
    signal.signal(signal.SIGINT, interrompido)
    manual = False
    ########## 1 --- Verifica se ocorreu alguma transação na carteira ---
    inicio = time.time()
    if address == '18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe': # Verifica se é um teste
        chave_publica = monitorar_mempool(address) # Busca a carteira
    else: #Se nao for teste
        manual = input('Deseja inserir a chave pública manualmente? (s/n): ').lower()

    if manual in sim:
        chave_publica = input("Insira a chave pública: ")
    else:
        chave_publica = monitorar_mempool(address)
        
    print (f'\n\n--------------------------------------------------------\n\nChave Pública: {chave_publica}\n\n--------------------------------------------------------------------------------\n')

    ########## 2 --- Quebrar Chave Pública na Privada
    if chave_publica:
        quebrar_chave(chave_publica, address)

    else:
        print('Chave Pública não encontrada, terminando script')
        return

    ########## 3 - Verifica se foi quebrada
    private_key = aguarda_quebra(240)
    if private_key:
        print(f"------\nPrivate Key HEX: {private_key} \n------")    
        private_key = converter_wif(address, private_key) # Converte pro formato WIF
        print (f'''\n------------------------------------------------------------------------------------------------------------------------
                \n---------------------------------Private Key WIF Compressed: {private_key}
                \n---------------------------------Minha Carteira = {destino}
                \n------------------------------------------------------------------------------------------------------------------------\n''')
    else:
        print('Não encontrada chave privada, terminando script')
        return
    
    ########## 4 - Inicia a Transferencia
    tx = transferir(private_key, destino)
    if tx:
        print('Verificando Saldo da sua carteira')
        verifica_saldo(destino)

    fim = time.time()
    print(f'O Código completo foi executado em: {(fim-inicio):.2f} segundos' )
    atexit.register(limpeza)

def configurar_keyhunt():
    range_inicial = input('\nInsira o Range Inicial (Range Carteira 66 = 20000000000000000): ')
    range_final = input('\nInsira o Range Final (Range Carteira 66 = 3ffffffffffffffff): ')
    k = int(input('\nInsira o valor do argumento -k (256): '))
    threads = int(input('Insira o numero de threads: '))
    if input('\nUsar -S (s/n): ').lower() in sim:
        argS = " -S"  
    else:
        argS='None'
    if input('\nUsar -R (s/n): ').lower() in sim:
        argR = " -R"  
    else:
        argR='None'

    with open ('configuracoeskeyhunt.txt', 'w') as config:
        config.writelines([
            f"{range_inicial}\n",
            f"{range_final}\n",
            f"{k}\n",
            f"{threads}\n",
            f"{argS}\n",
            f"{argR}"
        ])

if __name__ == '__main__':
    limpeza()
    print('---\nIniciando Script, Atenção, esse script monitora as transações da carteira "alvo" e usa KEYHUNT pra quebrar a chave pública na privada, converte em WIF e tenta realizar uma transferencia para sua conta, o código ainda está em desenvolvimento, esteja pronto para transferir manualmente caso falhe.\n---\n')
    executar_teste = input('Deseja executar o teste na carteira 65? (s/n): ').lower() 
    if executar_teste in sim:
        address = '18ZMbwUFLMHoZBbfpCjUJQTCMCbktshgpe' ##Carteira do Puzzle 65
    else:
        address = input('Insira o endereço da carteira que deseja procurar: ')
    destino = input('Insira o endereço da sua carteira (ao deixar o campo vazio não tentará transferir): ')
    destino = 'Não Informado' if destino == '' else destino
    if input("Configurar o Keyhunt? (s/n): ").lower() in sim:
        configurar_keyhunt()
    

    main(address, destino)

