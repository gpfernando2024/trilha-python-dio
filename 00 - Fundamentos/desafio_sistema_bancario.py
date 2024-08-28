
class ContaBancaria:
    def __init__(self):
        self.saldo = 0.0
        self.saques = []
        self.depositos = []
        self.limite_saque_diario = 500.0
        self.max_saques_diarios = 3
    
    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.depositos.append(valor)
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido. Apenas valores positivos são permitidos.")

    
    def sacar(self, valor):
        if len(self.saques) < self.max_saques_diarios:
            if valor <= self.limite_saque_diario:
                if valor <= self.saldo:
                    self.saldo -= valor
                    self.saques.append(valor)
                    print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
                else:
                    print("Saldo insuficiente para realizar o saque.")

            else:
                print(f"Limite de saque excedido. O limite máximo por saque é de R$ {self.limite_saque_diario:.2f}.")

        else:
            print(f"Limite de {self.max_saques_diarios} saques diários atingido.")
    
    def extrato(self):
        if not self.saques and not self.depositos:
            print("Não foram realizadas movimentações.")
        else:
            print("\n================ EXTRATO ================")
            for dep in self.depositos:
                print(f"Depósito: R$ {dep:.2f}")
            for saq in self.saques:
                print(f"Saque: R$ {saq:.2f}")
            print(f"Saldo atual: R$ {self.saldo:.2f}")
    
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
