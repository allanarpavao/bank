import textwrap
from datetime import datetime
from v2.sistema_bancario import ContaCorrente, ContaIterador, Deposito, PessoaFisica, Saque


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

def log_transacao(func):
    def wrapper(*args, **kwargs):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tipo_transacao = func.__name__
        print(f"[{data_hora}] Transaçao: {tipo_transacao}")
        return func(*args, **kwargs)
    return wrapper

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]

    if not clientes_filtrados:
        print("\n@@@ Cliente não encontrado! @@@")
        return
    else:
        return clientes_filtrados[0]

def menu_novo_cliente(cpf, clientes):
    while True:
        resposta = input("Deseja criar novo usuário? S/N/Sair ")
        if resposta == "S":
            criar_cliente(cpf=cpf, clientes=clientes)
            return
        elif resposta == "N":
            return
        elif resposta == "Sair":
            quit()
        else:
            print("\n@@@ Operação inválida. @@@")
            continue
    
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

def menu_nova_conta(cliente, contas):
    while True:
        resposta = input("Deseja criar nova conta? S/N/Sair ")
        if resposta == "S":
            numero_conta = len(contas) + 1
            criar_conta(cliente, numero_conta, contas)
            return
        elif resposta == "N":
            return
        elif resposta == "Sair":
            quit()
        else:
            print("\n@@@ Operação inválida. @@@")
            continue

@log_transacao
def depositar(cliente, conta):
    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def sacar(cliente, conta):
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)
    cliente.realizar_transacao(conta, transacao)

@log_transacao
def exibir_extrato(conta, tipo_transacao=None):
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.gerar_relatorio(tipo_transacao=tipo_transacao)

    extrato = ""
    transacao_found = False

    for transacao in transacoes:
        transacao_found = True
        extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f} em {transacao['data']}"

    if not transacao_found:
        extrato = "Não foram realizadas movimentações."

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

@log_transacao
def criar_cliente(cpf, clientes):
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

@log_transacao
def criar_conta(cliente, numero_conta, contas):
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")


def listar_contas(contas):
    conta_iterador = ContaIterador(contas)
    for conta_info in conta_iterador:
        print("=" * 100)
        print(f"C/C: {conta_info['numero']}")
        print(f"Agência: {conta_info['agencia']}")
        print(f"Titular {conta_info['cliente']}")
        print(f"Saldo: R$ {conta_info['saldo']:.2f}")


def main():
    clientes = []
    contas = []
    
    while True:
        
        cpf = input("Informe o CPF do cliente: ")
        cliente = filtrar_cliente(cpf, clientes) # retorna o objeto cliente
        
        
        # Verifica se o cliente existe
        if cliente == None:
            menu_novo_cliente(cpf=cpf, clientes=clientes)
        
        # Verifica se há pelo menos uma conta atrelada ao cliente
        elif recuperar_conta_cliente(cliente) == None:    
            menu_nova_conta(cliente, contas)
              
        else:
            conta = recuperar_conta_cliente(cliente)
            while True:
                opcao = menu()
                if opcao == "d":
                    depositar(cliente, conta)

                elif opcao == "s":
                    sacar(cliente, conta)

                elif opcao == "e":
                    exibir_extrato(conta)

                elif opcao == "nc":
                    numero_conta = len(contas) + 1
                    criar_conta(cliente, numero_conta, contas)

                elif opcao == "lc":
                    listar_contas(contas)

                elif opcao == "q":
                    quit()
                
                else:
                    print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")
            
main()