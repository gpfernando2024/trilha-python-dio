import os

class ContaBancaria:
    def __init__(self):
        self.saldo = 0.0
        self.saques = []
        self.depositos = []
        self.limite_saque_diario = 500.0
        self.max_saques_diarios = 3

    def depositar(self, saldo, valor, extrato):
        """Recebe saldo, valor e extrato como argumentos posicionais."""
        if valor > 0:
            saldo += valor
            extrato.append({"tipo": "Depósito", "valor": valor})
            print("Transação de depósito efetuada com sucesso.")
            return saldo, extrato
        else:
            raise ValueError("Valor de depósito inválido. Apenas valores positivos são permitidos.")

    def sacar(self, *, saldo, valor, extrato, limite, numero_saques, limite_saques):
        if numero_saques < limite_saques:
            if valor <= limite:
                if valor <= saldo:
                    saldo -= valor
                    extrato.append({"tipo": "Saque", "valor": valor})
                    print("Transação de saque efetuada com sucesso.")
                else:
                    raise ValueError("Saldo insuficiente para realizar o saque.")
            else:
                raise ValueError(f"Limite de saque excedido. O limite máximo por saque é de R$ {limite:.2f}.")
        else:
            raise ValueError(f"Limite de {limite_saques} saques diários atingido.")
        return saldo, extrato

    def extrato(self):
        print("\n==================== EXTRATO ====================")
        print(f"{'Tipo':<15} {'Valor (R$)':>15}")
        print("=" * 50)
        if not self.depositos and not self.saques:
            print(f"{'Sem movimentações':<15} {'-':>15}")
        else:
            for item in self.depositos + self.saques:
                print(f"{item['tipo']:<15} {item['valor']:>15.2f}")
        print("=" * 50)
        print(f"{'Saldo atual':<15} {self.saldo:>15.2f}")
        print("=" * 50)


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.numero_conta = 1

    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def criar_usuario(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if any(user['cpf'] == cpf for user in self.usuarios):
            raise ValueError("CPF já cadastrado.")
        nome = input("Informe o nome do usuário: ")
        data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")
        self.usuarios.append({
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf,
            "endereco": endereco
        })
        print(f"Usuário {nome} criado com sucesso.")
        input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
        self.limpar_tela()

    def criar_conta_corrente(self, cpf):
        usuario = next((user for user in self.usuarios if user['cpf'] == cpf), None)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
        conta = {
            "agencia": "0001",
            "numero_conta": self.numero_conta,
            "usuario": usuario,
            "conta_bancaria": ContaBancaria()
        }
        self.contas.append(conta)
        self.numero_conta += 1
        print(f"Conta {conta['numero_conta'] - 1} criada para o usuário {usuario['nome']}.")
        input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
        self.limpar_tela()

    def listar_contas(self):
        if not self.contas:
            print("Nenhuma conta corrente cadastrada.")
        else:
            print("\n==================== CONTAS CORRENTES ====================")
            print(f"{'Agência':<10} {'Número da Conta':<20} {'Nome do Usuário':<30}")
            print("=" * 60)
            for conta in self.contas:
                print(f"{conta['agencia']:<10} {conta['numero_conta']:<20} {conta['usuario']['nome']:<30}")
            print("=" * 60)
        input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
        self.limpar_tela()

    def desativar_conta_corrente(self, numero_conta):
        conta = next((conta for conta in self.contas if conta['numero_conta'] == numero_conta), None)
        if not conta:
            raise ValueError("Conta não encontrada.")
        self.contas.remove(conta)
        print(f"Conta {numero_conta} desativada com sucesso.")
        input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
        self.limpar_tela()

    def menu(self):
        while True:
            self.limpar_tela()
            print("\n--- Menu ---")
            print("1. Criar Usuário")
            print("2. Criar Conta Corrente")
            print("3. Listar Contas Correntes")
            print("4. Desativar Conta Corrente")
            print("5. Realizar Depósito")
            print("6. Realizar Saque")
            print("7. Extrato")
            print("8. Sair")
            opcao = input("Escolha uma opção: ")
            
            self.limpar_tela()  # Limpa a tela antes de executar a ação

            if opcao == '1':
                cpf = input("Informe o CPF do usuário (somente números): ")
                try:
                    self.criar_usuario(cpf)
                except ValueError as e:
                    print(e)
                    input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
                    self.limpar_tela()

            elif opcao == '2':
                cpf = input("Informe o CPF do usuário (somente números): ")
                try:
                    self.criar_conta_corrente(cpf)
                except ValueError as e:
                    print(e)
                    input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
                    self.limpar_tela()

            elif opcao == '3':
                self.listar_contas()

            elif opcao == '4':
                numero_conta = int(input("Informe o número da conta a ser desativada: "))
                try:
                    self.desativar_conta_corrente(numero_conta)
                except ValueError as e:
                    print(e)
                    input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
                    self.limpar_tela()

            elif opcao == '5':
                numero_conta = int(input("Informe o número da conta para depósito: "))
                conta = next((conta for conta in self.contas if conta['numero_conta'] == numero_conta), None)
                if conta:
                    valor = float(input("Informe o valor para depósito: R$ "))
                    try:
                        saldo, extrato = conta['conta_bancaria'].depositar(
                            saldo=conta['conta_bancaria'].saldo,
                            valor=valor,
                            extrato=conta['conta_bancaria'].depositos
                        )
                        conta['conta_bancaria'].saldo = saldo
                        conta['conta_bancaria'].depositos = extrato
                    except ValueError as e:
                        print(e)
                    input("Pressione Enter para continuar...")
                    self.limpar_tela()
                else:
                    print("Conta não encontrada.")
                    input("Pressione Enter para continuar...")
                    self.limpar_tela()


            elif opcao == '6':
                numero_conta = int(input("Informe o número da conta para saque: "))
                conta = next((conta for conta in self.contas if conta['numero_conta'] == numero_conta), None)
                if conta:
                    valor = float(input("Informe o valor para saque: R$ "))
                    try:
                        saldo, extrato = conta['conta_bancaria'].sacar(
                            saldo=conta['conta_bancaria'].saldo,
                            valor=valor,
                            extrato=conta['conta_bancaria'].saques,
                            limite=conta['conta_bancaria'].limite_saque_diario,
                            numero_saques=len(conta['conta_bancaria'].saques),
                            limite_saques=conta['conta_bancaria'].max_saques_diarios
                        )
                        conta['conta_bancaria'].saldo = saldo
                        conta['conta_bancaria'].saques = extrato
                    except ValueError as e:
                        print(e)
                    input("Pressione Enter para continuar...")
                    self.limpar_tela()
                else:
                    print("Conta não encontrada.")
                    input("Pressione Enter para continuar...")
                    self.limpar_tela()



            elif opcao == '7':
                numero_conta = int(input("Informe o número da conta para ver o extrato: "))
                conta = next((conta for conta in self.contas if conta['numero_conta'] == numero_conta), None)
                if conta:
                    conta['conta_bancaria'].extrato()
                else:
                    print("Conta não encontrada.")
                input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
                self.limpar_tela()
            elif opcao == '8':
                self.limpar_tela()
                print("Saindo do sistema. Até mais!")
                break

            else:
                print("Opção inválida. Tente novamente.")
                input("Pressione Enter para continuar...")  # Espera o usuário pressionar Enter antes de limpar a tela
                self.limpar_tela()


# Exemplo de uso
banco = Banco()
banco.menu()
