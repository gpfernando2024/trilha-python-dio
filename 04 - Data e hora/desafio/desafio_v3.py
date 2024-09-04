from datetime import datetime

class ContaBancaria:
    def __init__(self):
        self.saldo = 0.0
        self.saques = []
        self.depositos = []
        self.transacoes = []
        self.limite_saque_diario = 500.0
        self.max_saques_diarios = 3
        self.max_depositos_diarios = 4
        self.max_extratos_diarios = 3
        self.max_transacoes_diarias = 10

    def transacoes_diarias(self):
        hoje = datetime.now().date()
        return [t for t in self.transacoes if t['data'].date() == hoje]

    def verificar_limite_transacoes(self):
        if len(self.transacoes_diarias()) >= self.max_transacoes_diarias:
            print(f"Você excedeu o limite de {self.max_transacoes_diarias} transações diárias.")
            return False
        return True

    def saques_diarios(self):
        hoje = datetime.now().date()
        return [s for s in self.saques if s['data'].date() == hoje]

    def depositos_diarios(self):
        hoje = datetime.now().date()
        return [d for d in self.depositos if d['data'].date() == hoje]

    def verificar_limite_saques(self):
        if len(self.saques_diarios()) >= self.max_saques_diarios:
            print(f"Você excedeu o limite de {self.max_saques_diarios} saques diários.")
            return False
        return True

    def verificar_limite_depositos(self):
        if len(self.depositos_diarios()) >= self.max_depositos_diarios:
            print(f"Você excedeu o limite de {self.max_depositos_diarios} depósitos diários.")
            return False
        return True

    def verificar_limite_extratos(self):
        extratos_hoje = len([t for t in self.transacoes_diarias() if t['tipo'] == 'Extrato'])
        if extratos_hoje >= self.max_extratos_diarios:
            print(f"Você excedeu o limite de {self.max_extratos_diarios} extratos diários.")
            return False
        return True

    def depositar(self, valor):
        if not self.verificar_limite_transacoes() or not self.verificar_limite_depositos():
            return

        if valor > 0:
            self.saldo += valor
            self.depositos.append({'valor': valor, 'data': datetime.now()})
            self.transacoes.append({'tipo': 'Depósito', 'valor': valor, 'data': datetime.now()})
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido. Apenas valores positivos são permitidos.")

    def sacar(self, valor):
        if not self.verificar_limite_transacoes() or not self.verificar_limite_saques():
            return

        if valor <= self.limite_saque_diario:
            if valor <= self.saldo:
                self.saldo -= valor
                self.saques.append({'valor': valor, 'data': datetime.now()})
                self.transacoes.append({'tipo': 'Saque', 'valor': valor, 'data': datetime.now()})
                print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
            else:
                print("Saldo insuficiente para realizar o saque.")
        else:
            print(f"Limite de saque excedido. O limite máximo por saque é de R$ {self.limite_saque_diario:.2f}.")

    def extrato(self):
        if not self.verificar_limite_transacoes() or not self.verificar_limite_extratos():
            return

        if not self.transacoes:
            print("Não foram realizadas movimentações.")
        else:
            print("\n================ EXTRATO ================")
            for transacao in self.transacoes:
                data_formatada = transacao['data'].strftime('%d/%m/%Y %H:%M:%S')
                print(f"{transacao['tipo']}: R$ {transacao['valor']:.2f} - {data_formatada}")
            print(f"Saldo atual: R$ {self.saldo:.2f}")
        
        # Adicionar a transação de extrato
        self.transacoes.append({'tipo': 'Extrato', 'valor': 0.0, 'data': datetime.now()})

    def menu(self):
        while True:
            print("\n--- Menu ---")
            print("1. Depositar")
            print("2. Sacar")
            print("3. Extrato")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                valor = float(input("Informe o valor para depósito: R$ "))
                self.depositar(valor)
            elif opcao == '2':
                valor = float(input("Informe o valor para saque: R$ "))
                self.sacar(valor)
            elif opcao == '3':
                self.extrato()
            elif opcao == '4':
                print("Saindo do sistema. Até mais!")
                break
            else:
                print("Opção inválida. Tente novamente.")

# Exemplo de uso
conta = ContaBancaria()
conta.menu()
