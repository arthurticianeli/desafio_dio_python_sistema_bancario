import datetime

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
LIMITE_DIARIO_SAQUE = 500
depositos = []
saques = []
extrato = ""
numero_saques_diarios = 0
LIMITE_SAQUES_DIARIOS = 3

# Operação de depósito

# Deve ser possível depositar valores positivos
# Todos os depósitos devem ser armazenados em uma variável

def operacao_deposito():
    global saldo

    valor_deposito = float(input("Digite o valor do depósito: "))

    is_deposito_positivo = valor_deposito > 0

    if is_deposito_positivo:
        saldo += valor_deposito
        depositos.append({"valor": valor_deposito, "data": datetime.datetime.now().replace(microsecond=0)})
        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
    else:
        print("Valor inválido, tente novamente.")

# Operação de saque

# Deve permitir 3 saques diários
# Deve permitir saques com limite de 500,00
# Caso o valor solicitado seja superior ao saldo da conta, exibir msg informando que "Saldo insuficiente"
# Caso o valor solicitado seja superior ao limite diário, exibir msg informando que "Limite diário excedido"
# Todos os saques devem ser armazenados em uma variável

def operacao_saque():
    global saldo
    global numero_saques_diarios
    global saques

    if numero_saques_diarios >= LIMITE_SAQUES_DIARIOS:
        print("Limite diário de saques excedido.")
        return

    valor_saque = float(input("Digite o valor do saque: "))

    is_saque_positivo = valor_saque > 0

    if not is_saque_positivo:
        print("Valor inválido, tente novamente.")
        return

    is_saque_menor_que_saldo = valor_saque <= saldo
    is_saque_menor_que_limite_diario = valor_saque <= LIMITE_DIARIO_SAQUE

    if is_saque_menor_que_saldo and is_saque_menor_que_limite_diario:
        saldo -= valor_saque
        numero_saques_diarios += 1
        saques.append({"valor": valor_saque, "data": datetime.datetime.now().replace(microsecond=0)})
        print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
    elif not is_saque_menor_que_saldo:
        print("Saldo insuficiente.")
    elif not is_saque_menor_que_limite_diario:
        print("Limite diário de saques excedido.")

# Operação de extrato

# Deve listar todos os depósitos e saques realizados
# Deve exibir o saldo atual da conta
# Usar o formato R$ xxx.xx

def operacao_extrato():
    global extrato

    operacoes = []

    for deposito in depositos:
        operacoes.append({"tipo": "Depósito", "valor": deposito["valor"], "data": deposito["data"]})

    for saque in saques:
        operacoes.append({"tipo": "Saque", "valor": saque["valor"], "data": saque["data"]})

    operacoes_ordenadas_por_data = sorted(operacoes, key=lambda operacao: operacao["data"])

    extrato = "Extrato\n\n"

    for operacao in operacoes_ordenadas_por_data:
        tipo = operacao["tipo"]
        valor = operacao["valor"]
        data = operacao["data"]

        extrato += f"{tipo} de R$ {valor:.2f} em {data}\n"

    extrato += f"\nSaldo atual: R$ {saldo:.2f}"

    print(extrato)


while True:

    opcao = input(menu)

    if opcao == "d":
        operacao_deposito()

    elif opcao == "s":
        operacao_saque()

    elif opcao == "e":
        operacao_extrato()

    elif opcao == "q":
        break

    else:
        print("Opção inválida, por favor selecione novamente a opção desejada.")