"""Testes para o gerenciador de criptografia."""

import pytest
from sabrina.crypto import CryptoManager


def test_encrypt_decrypt():
    """Testa criptografia e descriptografia."""
    crypto = CryptoManager()
    plaintext = "minha_senha_secreta"
    encrypted = crypto.encrypt(plaintext)
    decrypted = crypto.decrypt(encrypted)
    assert plaintext == decrypted


def test_encrypt_different_outputs():
    """Testa que encriptações geram outputs diferentes."""
    crypto = CryptoManager()
    plaintext = "mesma_senha"
    encrypted1 = crypto.encrypt(plaintext)
    encrypted2 = crypto.encrypt(plaintext)
    # Fernet adiciona timestamp, então os resultados devem ser diferentes
    assert encrypted1 != encrypted2


def test_decrypt_invalid_raises_error():
    """Testa que descriptografia inválida lança erro."""
    crypto = CryptoManager()
    with pytest.raises(ValueError):
        crypto.decrypt("invalid_encrypted_data")


def test_wrong_master_password():
    """Testa que senha mestre errada não pode descriptografar."""
    crypto1 = CryptoManager(master_password="senha1")
    encrypted = crypto1.encrypt("dados_secretos")

    crypto2 = CryptoManager(master_password="senha2")
    with pytest.raises(ValueError):
        crypto2.decrypt(encrypted)


def test_verify_password():
    """Testa verificação de senha mestre."""
    crypto = CryptoManager(master_password="minha_senha")
    assert crypto.verify_password("minha_senha") is True
    assert crypto.verify_password("senha_errada") is False