
from abc import ABC, abstractmethod, abstractproperty
import datetime
import textwrap
from typing import List

CPF_PROMPT = "Digite o CPF do cliente: "
CLIENTE_NAO_ENCONTRADO = "Cliente não encontrado."

def menu():
    menu = """
    ========= Menu =========

    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Cadastrar Conta Corrente
    [u] Cadastrar usuário
    [l] Listar contas
    [q] Sair

    => """

    return input(textwrap.dedent(menu))

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass
    
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao: Transacao):
        return transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
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
    
    def sacar(self, valor_saque):
        saldo = self._saldo
    
        is_saque_negativo = valor_saque < 0
        is_saque_maior_que_saldo = valor_saque > saldo

        if is_saque_negativo:
            print("Valor inválido, tente novamente.")
            return False

        if is_saque_maior_que_saldo:
            print("Saldo insuficiente.")
            return False

        self._saldo -= valor_saque
        Saque(valor_saque)
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
        return True

    def depositar(self, valor_deposito):

        is_deposito_negativo = valor_deposito <= 0

        if is_deposito_negativo:
            print("Valor inválido, tente novamente.")
            return False
     
        self._saldo += valor_deposito
        Deposito(valor_deposito)
        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_valor_diario=500, limite_saques_diarios=3):
        super().__init__(numero, cliente)
        self._limite_valor_diario = limite_valor_diario
        self._limite_saques_diarios = limite_saques_diarios

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"]
        )

        excedeu_limite = valor > self._limite_valor_diario
        excedeu_limite_saques = numero_saques >= self._limite_saques_diarios

        if excedeu_limite:
            print(f"Valor excede o limite diário de saque de R$ {self._limite_valor_diario:.2f}.")
            return False
        
        if excedeu_limite_saques:
            print(f"Limite diário de saques excedido. Limite: {self._limite_saques_diarios}")
            return False
        
        return super().sacar(valor)

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            Conta Corrente:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """
        
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.datetime.now().replace(microsecond=0)
        })


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta: Conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            return True

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta: Conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
            return True

def cpf_sem_caracteres_especiais(cpf):
    return cpf.replace(".", "").replace("-", "")

def filtrar_cliente(clientes: List[PessoaFisica], cpf_cliente: str):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf_sem_caracteres_especiais(cpf_cliente)]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente: PessoaFisica):
    if not cliente.contas:
        print("Cliente não possui contas.")
        return
    
    return cliente.contas[0]

def operacao_deposito(clientes: List[PessoaFisica]):

    cpf_cliente = input(CPF_PROMPT)
    cliente = filtrar_cliente(clientes, cpf_cliente)

    if not cliente:
        print(CLIENTE_NAO_ENCONTRADO)
        return

    valor_deposito = float(input("Digite o valor do depósito: "))

    transacao = Deposito(valor_deposito)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def operacao_saque(clientes: List[PessoaFisica]):
    cpf_cliente = input(CPF_PROMPT)
    cliente = filtrar_cliente(clientes, cpf_cliente)

    if not cliente:
        print(CLIENTE_NAO_ENCONTRADO)
        return

    valor_saque = float(input("Digite o valor do saque: "))
    transacao = Saque(valor_saque)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes: List[PessoaFisica]):
    cpf_cliente = input(CPF_PROMPT)
    cliente: Cliente = filtrar_cliente(clientes, cpf_cliente)

    if not cliente:
        print(CLIENTE_NAO_ENCONTRADO)
        return

    conta: Conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    transacoes: List[Transacao] = conta.historico.transacoes

    print("\n ================ EXTRATO ================")

    extrato = ""
    if not transacoes:
        extrato = "Nenhuma transação realizada."

    else:
        for transacao in transacoes:
            extrato += f"{transacao['data']} - {transacao['tipo']}: R$ {transacao['valor']:.2f}\n"

    print(extrato)
    print(f"Saldo atual: R$ {conta.saldo:.2f}")
    print("\n =========================================")

def cadastrar_cliente(clientes: List[PessoaFisica]):

    interromper_cadastro = False

    while True:
        cpf = input("Digite o CPF do usuário: ")
        if filtrar_cliente(clientes, cpf):
            print("""CPF já cadastrado.
                
                [1] - Tentar novamente
                [2] - Voltar ao menu principal
            """)
            opcao = input("=> ")
            if opcao == "2":
                interromper_cadastro = True
                break
        else:
            break

    if interromper_cadastro:
        return
    
    nome = input("Digite o nome do usuário: ")
    data_nascimento = input("Digite a data de nascimento do usuário: ")
    endereco = input("Digite o endereco do usuário (logradouro, nro - bairro - cidade/estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("Usuário cadastrado com sucesso.")

def criar_conta_corrente(numero_conta: int, clientes: List[PessoaFisica], contas: List[Conta]):

    interromper_cadastro = False
    
    while True:
        cpf = input("Digite o CPF do usuário: ")  
        cliente = filtrar_cliente(clientes, cpf)

        if not cliente:
            print("""Cliente não encontrado.
                
                [1] - Tentar novamente
                [2] - Voltar ao menu principal
            """)
            opcao = input("=> ")
            if opcao == "2":
                interromper_cadastro = True
                break
        else:
            break

    if interromper_cadastro:
        return
    
    conta = ContaCorrente.nova_conta(numero=numero_conta, cliente=cliente)

    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta corrente criada com sucesso.")

def listar_contas(contas: List[Conta]):

    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:

        opcao = menu()

        if opcao == "d":
            operacao_deposito(clientes)
           
        elif opcao == "s":
            operacao_saque(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "u":
            cadastrar_cliente(clientes)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Opção inválida, por favor selecione novamente a opção desejada.")

main()
