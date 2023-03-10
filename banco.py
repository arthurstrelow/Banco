import base64
from datetime import datetime


class ContaBancaria:
    datahora = datetime.today().strftime('%d/%m/%Y - %H:%M:%S')
    def __init__(self, numero='000', agencia='0', tipo='POUPANÇA', saldo=0.0):
        self.numero = numero  # 8 Números
        self.agencia = agencia  # 4 Números
        self.tipo = tipo  # Conta Corrente ou Poupança
        self.saldo = saldo

        try: #Verifica se o arquivo DATABASE e LOGS existem, caso não existir ele cria, se sim não faz nada.
            arquivo = open('database.txt', 'rt')
            logs = open('logs.txt', 'rt')
        except FileNotFoundError:
            arquivo = open('database.txt', 'wt+')
            logs = open('logs.txt', 'wt+')
        arquivo.close()
        logs.close()

    def cadastrarConta(self):
        arqVeri = open('database.txt', 'rt')
        armazenaconta = ''
        for conta in arqVeri:
            armazenaconta += f'{conta.split(";")[0]}\n' #Armazena tudo em uma variavel para fazer a verificação de conta repetida
        if self.numero in armazenaconta: #Evitar repetições de conta
            return
        else:
            criacao = open('database.txt', 'at')
            criacao.write(f'{self.numero};{self.agencia};{self.tipo};{self.saldo};\n')
            criacao.close()
        self.logs(f'A conta => "{self.numero}" foi criada! ({self.datahora})')
        arqVeri.close()

    def exibirDados(self):
        try:
            dados = open('database.txt', 'rt')
            armazenaconta = ''
            armazenaag = []
            armazenatipo = []
            armazenasaldo = []
            for conta in dados:
                armazenaconta += f'{conta.split(";")[0]}\n'
                armazenaag.append(conta.split(";")[1])
                armazenatipo.append(conta.split(";")[2])
                armazenasaldo.append(conta.split(";")[3])
            indice = int(armazenaconta.index(self.numero) / 9) #Esse calcula é para determinar o indice pela posição da primeira string de cada conta
            if self.numero in armazenaconta:
                print(f'Número da Conta: {armazenaconta[armazenaconta.index(self.numero):armazenaconta.index(self.numero) + 8]}')
                print(f'Agencia: {armazenaag[indice]}')
                print(f'Tipo: {armazenatipo[indice]}')
                print(f'SALDO: R$ {armazenasaldo[int(indice)]}')
            self.logs(f'A conta => "{self.numero}" consultou seus dados ({self.datahora})')
            dados.close()
        except:
            print('Conta não Existe. Opção [1] para criar uma Nova Conta')

    def areaADM(self, senha='0'): #Mostra todas as contas
        if senha == '000555':
            dados = open('database.txt', 'rt')
            for linha in dados:
                dado = linha.split(';')
                final = f'Número da conta: {dado[0]} - Agencia: {dado[1]} - Tipo da conta: {dado[2]} - Saldo: R$ {dado[3]}'
                print(final)
            dados.close()

    def exibirSaldo(self):
        try:
            dados = open('database.txt', 'rt')
            armazenaconta = ''
            armazenasaldo = []
            for conta in dados:
                armazenaconta += f'{conta.split(";")[0]}\n'
                armazenasaldo.append(conta.split(";")[3])
            indice = int(armazenaconta.index(self.numero) / 9)
            if self.numero in armazenaconta:
                print(f'Número da Conta: {armazenaconta[armazenaconta.index(self.numero):armazenaconta.index(self.numero) + 8]}')
                print(f'SALDO: R$ {armazenasaldo[int(indice)]}')
            self.logs(f'A conta => "{self.numero}" consultou seu saldo ({self.datahora})')
            dados.close()
        except:
            print('Conta não Existe. Opção [1] para criar uma Nova Conta')

    def logs(self, log):
        database = open('logs.txt', 'at')
        codificado = base64.b64encode(log.encode('ascii'))
        codificado_ascii = codificado.decode('ascii')
        database.write(f'{codificado_ascii}\n')
        database.close()

    def transacao(self,quantia, operacao):
        try:
            dados = open('database.txt', 'rt')
            valornovo = 0
            msg = ''
            permissao = False
            armazenaconta = ''
            armazenasaldo = []
            armazenaag = []
            armazenatipo = []
            for conta in dados:
                armazenaconta += f'{conta.split(";")[0]}\n'
                armazenasaldo.append(conta.split(";")[3])
                armazenaag.append(conta.split(";")[1])
                armazenatipo.append(conta.split(";")[2])
            indice = int(armazenaconta.index(self.numero) / 9)
            if operacao == 'DEPOSITO':
                valornovo = quantia + float(armazenasaldo[indice])
                msg = f'Deposito Efetuado com Sucesso! Dinheiro em conta R$ {valornovo}'
                permissao = True
            elif operacao == 'SAQUE':
                if quantia <= float(armazenasaldo[indice]): # So saca se tiver o dinheiro em conta
                    valornovo = float(armazenasaldo[indice]) - quantia
                    msg = f'Saque Efetuado. Valor em conta R$ {valornovo}'
                    permissao = True
                else:
                    msg = f'Saldo Insuficiente! Você possui em conta R$ {armazenasaldo[indice]}'
            if permissao:
                with open('database.txt', 'r') as f:
                    texto = f.readlines()
                with open('database.txt', 'w') as f:
                    for i in texto:
                        if texto.index(i) == indice:
                            f.write(f'{self.numero};{armazenaag[indice]};{armazenatipo[indice]};{valornovo};\n')
                        else:
                            f.write(i)
                self.logs(f'A conta => "{self.numero}" fez um {operacao} de {quantia} ({self.datahora})')
            print(msg)
        except:
            print('Conta não Existe. Opção [1] para criar uma Nova Conta')