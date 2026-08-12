"""Módulo de criptografia para proteção de senhas."""

import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2


class CryptoManager:
    """Gerencia criptografia e descriptografia de senhas."""

    def __init__(self, master_password: str = "sabrina12345"):
        """
        Inicializa o gerenciador de criptografia.

        Args:
            master_password: Senha mestre para derivar a chave (padrão: "sabrina12345")
        """
        self.master_password = master_password
        self._cipher = self._generate_cipher()

    def _generate_cipher(self) -> Fernet:
        """Gera uma cifra Fernet a partir da senha mestre."""
        # Usa PBKDF2 para derivar uma chave a partir da senha mestre
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b"sabrina_salt_2024",  # Salt fixo para consistência
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(
            kdf.derive(self.master_password.encode())
        )
        return Fernet(key)

    def encrypt(self, plaintext: str) -> str:
        """Criptografa um texto.

        Args:
            plaintext: Texto a criptografar

        Returns:
            str: Texto criptografado em base64
        """
        encrypted = self._cipher.encrypt(plaintext.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, ciphertext: str) -> str:
        """Descriptografa um texto.

        Args:
            ciphertext: Texto criptografado em base64

        Returns:
            str: Texto descriptografado

        Raises:
            ValueError: Se a criptografia for inválida
        """
        try:
            encrypted = base64.b64decode(ciphertext.encode())
            decrypted = self._cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            raise ValueError("Falha ao descriptografar. Senha mestre incorreta?") from e

    def verify_password(self, master_password: str) -> bool:
        """Verifica se a senha mestre está correta.

        Args:
            master_password: Senha a verificar

        Returns:
            bool: True se a senha está correta
        """
        return master_password == self.master_password