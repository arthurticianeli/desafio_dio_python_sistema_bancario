import datetime

menu = """
========= Menu =========

[d] Depositar
[s] Sacar
[e] Extrato
[c] Cadastrar Conta Corrente
[u] Cadastrar usuário
[q] Sair

=> """

def operacao_deposito(saldo, depositos, /):

    valor_deposito = float(input("Digite o valor do depósito: "))

    is_deposito_positivo = valor_deposito > 0

    if is_deposito_positivo:
        saldo += valor_deposito
        depositos.append({"valor": valor_deposito, "data": datetime.datetime.now().replace(microsecond=0)})
        print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso.")
        
        return saldo, depositos
    elif not is_deposito_positivo:
        print("Valor inválido, tente novamente.")

def verificar_atingiu_limite_valor_saques_diarios(*,valor_saque, saques, valor_limite_diario_saque):

    data_atual = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    valor_total_saques_dia_atual = sum([saque["valor"] for saque in saques if saque["data"] >= data_atual])

    is_limite_atingido = valor_total_saques_dia_atual >= valor_limite_diario_saque or valor_saque > valor_limite_diario_saque

    if(is_limite_atingido):
        print(f"Limite diário de saques excedido. Limite: R$ {valor_limite_diario_saque:.2f}")

    return is_limite_atingido

def operacao_saque(*, saldo, saques, valor_limite_diario_saque):

    valor_saque = float(input("Digite o valor do saque: "))

    is_saque_negativo = valor_saque < 0
    is_saque_maior_que_saldo = valor_saque >= saldo

    if is_saque_negativo:
        print("Valor inválido, tente novamente.")
        return

    if is_saque_maior_que_saldo:
        print("Saldo insuficiente.")
        return
    
    if verificar_atingiu_limite_valor_saques_diarios(valor_saque=valor_saque, saques=saques, valor_limite_diario_saque=valor_limite_diario_saque):
        return
    
    saldo -= valor_saque
    saques.append({"valor": valor_saque, "data": datetime.datetime.now().replace(microsecond=0)})
    print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso.")
    return saldo, saques

def operacao_extrato(depositos, /, saques, *, saldo):
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

def verificar_cpf_existe(usuarios, cpf_sem_caracteres_especiais):
    cpf_existe = cpf_sem_caracteres_especiais in [usuario["cpf"] for usuario in usuarios]
    return cpf_existe

def cadastrar_usuario(usuarios):

    interromper_cadastro = False

    nome = input("Digite o nome do usuário: ")

    while True:
        cpf = input("Digite o CPF do usuário: ")
        cpf_sem_caracteres_especiais = cpf.replace(".", "").replace("-", "")
        if verificar_cpf_existe(usuarios, cpf_sem_caracteres_especiais):
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
    
    data_nascimento = input("Digite a data de nascimento do usuário: ")
    logradouro = input("Digite o logradouro do usuário: ")
    numero = input("Digite o número do usuário: ")
    bairro = input("Digite o bairro do usuário: ")
    cidade = input("Digite a cidade do usuário: ")
    estado = input("Digite o estado do usuário: ")

    usuarios.append({
        "nome": nome,
        "cpf": cpf_sem_caracteres_especiais,
        "data_nascimento": data_nascimento,
        "endereco": f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}",
        "contas_correntes": []
    })

    print("Usuário cadastrado com sucesso.")

    return usuarios

def criar_conta_corrente(usuarios, contas, numero_agencia):

    interromper_cadastro = False
    
    while True:
        cpf = input("Digite o CPF do usuário: ")
        cpf_sem_caracteres_especiais = cpf.replace(".", "").replace("-", "")
    
        usuario = [usuario for usuario in usuarios if usuario["cpf"] == cpf_sem_caracteres_especiais]

        if not usuario:
            print("""Usuário não encontrado.
                
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
        return usuarios, contas
    
    conta = {
        "usario_vinculado": usuario[0]["cpf"],
        "agencia": numero_agencia,
        "numero": len(contas) + 1
    }

    usuario[0]["contas_correntes"].append(conta)

    contas.append(conta)

    print("Conta corrente criada com sucesso.")

    return usuarios, contas

def verificar_atingiu_limite_transacoes_diarias(*, depositos, saques, limite_transacoes_diarias):

    data_atual = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    saques_dia_atual = [saque for saque in saques if saque["data"] >= data_atual]
    depositos_dia_atual = [deposito for deposito in depositos if deposito["data"] >= data_atual]

    is_limite_atingido = len(saques_dia_atual) + len(depositos_dia_atual) >= limite_transacoes_diarias

    if(is_limite_atingido):
        print("Limite de transações diárias alcançado.")
 
    return is_limite_atingido

def verificar_atingiu_limite_saques_diarios(*, saques, limites_saques_diarios):
    
    data_atual = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    saques_dia_atual = [saque for saque in saques if saque["data"] >= data_atual]

    is_limite_atingido = len(saques_dia_atual) >= limites_saques_diarios

    if(is_limite_atingido):
        print("Limite diário de saques excedido.")

    return is_limite_atingido

def main():
    VALOR_LIMITE_DIARIO_SAQUE = 500
    LIMITE_SAQUES_DIARIOS = 3
    LIMITE_TRANSACOES_DIARIAS = 10
    NUMERO_AGENCIA = "0001"
    
    saldo = 0
    depositos = []
    saques = []

    usuarios = []
    contas = []

    print(usuarios)

    while True:

        opcao = input(menu)

        if opcao == "d":
            if not(
                verificar_atingiu_limite_transacoes_diarias(depositos=depositos, saques=saques, limite_transacoes_diarias=LIMITE_TRANSACOES_DIARIAS) and 
                verificar_atingiu_limite_saques_diarios(saques=saques, limites_saques_diarios=LIMITE_SAQUES_DIARIOS)):
                    saldo, depositos = operacao_deposito(
                    saldo, 
                    depositos
                    )

        elif opcao == "s":
            if not(verificar_atingiu_limite_saques_diarios(saques=saques, limites_saques_diarios=LIMITE_SAQUES_DIARIOS)):                  
                saldo, saques = operacao_saque(
                    saldo=saldo, 
                    saques=saques,
                    valor_limite_diario_saque=VALOR_LIMITE_DIARIO_SAQUE
                    )

        elif opcao == "e":
            operacao_extrato(
                depositos, 
                saques, 
                saldo=saldo
            )

        elif opcao == "u":
            usuarios = cadastrar_usuario(usuarios)

        elif opcao == "c":
            usuarios, contas = criar_conta_corrente(usuarios, contas, NUMERO_AGENCIA)

        elif opcao == "q":
            break

        else:
            print("Opção inválida, por favor selecione novamente a opção desejada.")

main()
