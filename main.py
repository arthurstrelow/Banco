from time import sleep
from random import randint
from banco import ContaBancaria

print('''BEM VINDO AO BANCO NACIONAL''')
while True:
    opcao = input('''O QUE DESEJA?
[1] CRIAR CONTA
[2] VER SALDO
[3] VER INFORMAÇÕES DA SUA CONTA
[4] DEPOSITAR
[5] SACAR
[6] SAIR
=> ''')
    if opcao == '1':
        geraConta = randint(10000000, 99999999)
        geraAg = randint(1000, 9999)
        banco = ContaBancaria(str(geraConta), str(geraAg))
        banco.cadastrarConta()
        sleep(3)
        print(f'\n\nNúmero da Conta: {geraConta}\nAgencia: {geraAg}\n\n')
        sleep(6)
    elif opcao == '2':
        banco = ContaBancaria(input('\nDigite sua Conta => '))
        banco.exibirSaldo()
        sleep(4)
    elif opcao == '3':
        banco = ContaBancaria(input('\nDigite sua Conta => '))
        banco.exibirDados()
        sleep(4)
    elif opcao == '4':
        banco = ContaBancaria(input('\nDigite sua Conta => '))
        banco.transacao(float(input('Deseja Depositar quanto? ')), 'DEPOSITO')
        sleep(4)
    elif opcao == '5':
        banco = ContaBancaria(input('\nDigite sua Conta => '))
        banco.transacao(float(input('Deseja Sacar quanto? ')), 'SAQUE')
        sleep(4)
    elif opcao == '6':
        break
    else:
        print(f'{opcao} não é uma opção válida!\n\n')
        sleep(2)
