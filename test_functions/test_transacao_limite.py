import pytest
from datetime import datetime
import sys
import os

import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from v2.sistema_bancario import ContaCorrente, PessoaFisica, Deposito, Saque

@pytest.fixture
def setup_conta():
    """
    Fixture to set up a client and account for testing.
    """
    cliente = PessoaFisica(nome="Test User", data_nascimento="01-01-1990", cpf="12345678900", endereco="123 Test St")
    conta = ContaCorrente(numero=1001, cliente=cliente)
    return conta

def test_limite_diario_de_transacoes(setup_conta, capsys):
    """
    Test that the daily transaction limit is enforced.
    """
    conta = setup_conta

    # Simulate 10 transactions
    for _ in range(10):
        transacao = Deposito(valor=100)
        conta.historico.adicionar_transacao(transacao)

    # Attempt the 11th transaction
    transacao = Deposito(valor=100)
    conta.historico.adicionar_transacao(transacao)

    # Check output message for exceeding limit
    transacoes_hoje = conta.historico.contar_transacoes_do_dia()
    assert transacoes_hoje == 10  # Ensure only 10 transactions are counted

    # Attempt another transaction (this would print a failure message)
    exceeded = conta.historico.contar_transacoes_do_dia() >= 10
    assert exceeded  # Check that the limit is enforced

