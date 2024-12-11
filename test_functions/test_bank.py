import pytest
from datetime import datetime

from sistema_bancario import ContaCorrente, PessoaFisica

def test_deposit():
    cliente = PessoaFisica("Alice", datetime(1990, 5, 15), "12345678900", "123 Street Name")
    conta = ContaCorrente(1001, cliente)
    conta.depositar(500)
    assert conta.saldo == 500

def test_withdraw():
    cliente = PessoaFisica("Alice", datetime(1990, 5, 15), "12345678900", "123 Street Name")
    conta = ContaCorrente(1001, cliente)
    conta.depositar(500)
    result = conta.sacar(200)
    assert result is True
    assert conta.saldo == 300
