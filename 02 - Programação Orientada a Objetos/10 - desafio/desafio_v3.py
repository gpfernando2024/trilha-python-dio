import textwrap
import os
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Função para limpar a tela do terminal
def limpar_tela():
    sistema = os.name
    if sistema == 'posix':  # Para sistemas Unix (Linux/macOS)
        os.system('clear')
    elif sistema == 'nt':  # Para Windows
        os.system('cls')

# Classe que representa um cliente do banco
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Subclasse de Cliente, que representa uma pessoa física
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe que representa uma conta bancária
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

# Subclasse de Conta que implementa uma conta corrente
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Classe que registra o histórico de transações de uma conta
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "numero_banco": transacao.numero_banco  # Adicionado
            }
        )

# Classe abstrata para representar uma transação (sacar ou depositar)
class Transacao(ABC):
    def __init__(self, valor, numero_banco):
        self._valor = valor
        self._numero_banco = numero_banco
    @property
    @abstractproperty
    def valor(self):
        return self._valor
    
    def numero_banco(self):
        return self._numero_banco

    @abstractclassmethod
    def registrar(self, conta, numero_banco):
        pass

# Classe que representa uma transação de saque
class Saque(Transacao):
    def __init__(self, valor, numero_conta):
        super().__init__(valor, numero_conta)
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Classe que representa uma transação de depósito
class Deposito(Transacao):
    def __init__(self, valor, conta):
         super().__init__(valor, conta)

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Função que exibe o menu principal
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para filtrar clientes pelo CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função para recuperar a conta de um cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    return cliente.contas[0]

# Função que filtra as contas de um cliente e verifica se a conta existe
def filtrar_conta_cliente(cliente, numero_conta):
    """Função que filtra as contas de um cliente e verifica se a conta existe"""
    # Verificando se cliente possui contas
    if not hasattr(cliente, 'contas') or not cliente.contas:
        print("Cliente não possui contas cadastradas.")
        return None

    # Verificando se a conta existe
    for conta in cliente.contas:
        if str(conta.numero) == numero_conta:
            return conta
    
    print(f"Conta com número {numero_conta} não encontrada.")
    return None



# Função para realizar um depósito
def depositar(clientes):
    numero_conta = input("Informe o número da conta: ")
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    conta = filtrar_conta_cliente(cliente, numero_conta)
    
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor,conta=numero_conta)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para realizar um saque
def sacar(clientes):
    numero_conta = input("Informe o número da conta: ")
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    conta = filtrar_conta_cliente(cliente, numero_conta)

    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return
        
    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor,conta)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para exibir o extrato da conta
def exibir_extrato(clientes):
    numero_conta = input("Informe o número da conta: ")
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)
    conta = filtrar_conta_cliente(cliente, numero_conta)
    
    if not conta:
        print("\n@@@ Conta não encontrada! @@@")
        return

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    #if not conta:
    #    return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

# Função para criar um novo cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

# Função para criar uma nova conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    cliente.adicionar_conta(conta)
    contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

# Função para listar contas
def listar_contas(contas):
    if not contas:
        print("\n@@@ Nenhuma conta registrada! @@@")
        return

    for conta in contas:
        print(conta)

# Função principal que executa o menu e as operações
def main():
    clientes = []
    contas = []
    numero_conta = 1

    while True:
        opcao = menu()
        limpar_tela()
        
        if opcao == 'd':
            depositar(clientes)
        elif opcao == 's':
            sacar(clientes)
        elif opcao == 'e':
            exibir_extrato(clientes)
        elif opcao == 'nc':
            criar_conta(numero_conta, clientes, contas)
            numero_conta += 1
        elif opcao == 'lc':
            listar_contas(contas)
        elif opcao == 'nu':
            criar_cliente(clientes)
        elif opcao == 'q':
            print("Saindo...")
            break
        else:
            print("\n@@@ Opção inválida! @@@")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
