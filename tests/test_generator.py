"""Testes para o gerador de senhas."""

import pytest
from sabrina.generator import PasswordGenerator


def test_generate_default():
    """Testa geração de senha com configuração padrão."""
    gen = PasswordGenerator()
    password = gen.generate()
    assert len(password) == 16
    assert isinstance(password, str)


def test_generate_custom_length():
    """Testa geração com comprimento customizado."""
    gen = PasswordGenerator(length=32)
    password = gen.generate()
    assert len(password) == 32


def test_generate_minimum_length():
    """Testa que o comprimento mínimo é 4."""
    gen = PasswordGenerator(length=2)
    password = gen.generate()
    assert len(password) == 4


def test_generate_no_special_chars():
    """Testa geração sem caracteres especiais."""
    gen = PasswordGenerator(use_special_chars=False, length=100)
    password = gen.generate()
    assert len(password) == 100
    assert not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)


def test_generate_multiple():
    """Testa geração de múltiplas senhas."""
    gen = PasswordGenerator()
    passwords = gen.generate_multiple(5)
    assert len(passwords) == 5
    assert len(set(passwords)) == 5  # Todas únicas


def test_validate_strength_weak():
    """Testa validação de senha fraca."""
    gen = PasswordGenerator()
    result = gen.validate_strength("123")
    assert result["score"] <= 2


def test_validate_strength_strong():
    """Testa validação de senha forte."""
    gen = PasswordGenerator()
    result = gen.validate_strength("MyP@ssw0rd!Secure")
    assert result["score"] >= 4


def test_validate_strength_feedback():
    """Testa feedback de validação."""
    gen = PasswordGenerator()
    result = gen.validate_strength("abc")
    assert "feedback" in result
    assert len(result["feedback"]) > 0