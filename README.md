
## Introdução

**`Bot`** criado para monitorar a carteira solicitada em busca da sua chave pública, iniciar a quebra usando KEYHUNT no **`Linux`**

**`ATENÇÃO:`** Instale e compile o keyhunt normalmente conforme instruções do criador https://github.com/albertobsd/keyhunt

O meu código está livre para ser alterado como desejar.

## Instalação

#### `Instale e compile o keyhunt conforme instruções do criador: https://github.com/albertobsd/keyhunt`
Execute todos esses comandos no terminal:

```
git clone https://github.com/ataidefcjr/desafio-keyhunt
cd desafio-keyhunt
pip install -r requirements.txt
cd ..
mv desafio-keyhunt/* keyhunt/
rm -r -f desafio-keyhunt
```
## Como usar
Abra o terminal, navegue até a pasta do keyhunt `cd keyhunt` e execute o comando `python main.py`

Será solicitado o endereço da carteira a ser monitada e o endereço da sua carteira para tentativa de transferencia, quando encontrado a chave pública será iniciado a quebra usando o keyhunt.



## Observações Importantes:
* O range da chave privada foi limitado para as carteiras `65 e 66` do puzzle, ajuste em hashs.py linhas 10 e 11 se necessário.

* Ao efetivar a quebra o bot irá tentar enviar os fundos para sua carteira usando a biblioteca bit, porém em teste realizado durante a live do desafio no canal https://www.youtube.com/@investidorint não funcionou como o esperado, pelo menos nesse caso em específico, mostrando saldo 0 para o endereço.

* Tentei tambem importar na carteira Electrum logo que a transferencia do bot falhou (cerca de 5 segundos) e tambem acusou saldo 0 e não permitiu iniciar transferência.

* A `WIF` será exibida no console assim que quebrada a criptografia para que possa tentar por outros meios.

* Alguns arquivos ficarão salvos no diretório do repositório após encontrar alguma chave.`PublicKey.txt` contendo as chaves públicas encontradas e `WIF.txt` com as chaves WIF encontradas.

## Doações

* Se conseguir resgatar e quiser doar alguns BTC pro papai aqui: `bc1qych3lyjyg3cse6tjw7m997ne83fyye4des99a9`