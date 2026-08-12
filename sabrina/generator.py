"""Módulo gerador de senhas aleatórias e seguras."""

import random
import string
from typing import Optional


class PasswordGenerator:
    """Gera senhas aleatórias com opções personalizáveis."""

    def __init__(
        self,
        length: int = 16,
        use_uppercase: bool = True,
        use_lowercase: bool = True,
        use_numbers: bool = True,
        use_special_chars: bool = True,
    ):
        """
        Inicializa o gerador de senhas.

        Args:
            length: Comprimento da senha (padrão: 16)
            use_uppercase: Incluir letras maiúsculas (padrão: True)
            use_lowercase: Incluir letras minúsculas (padrão: True)
            use_numbers: Incluir números (padrão: True)
            use_special_chars: Incluir caracteres especiais (padrão: True)
        """
        self.length = max(4, length)  # Mínimo de 4 caracteres
        self.use_uppercase = use_uppercase
        self.use_lowercase = use_lowercase
        self.use_numbers = use_numbers
        self.use_special_chars = use_special_chars

    def _build_charset(self) -> str:
        """Constrói o conjunto de caracteres válidos."""
        charset = ""
        if self.use_uppercase:
            charset += string.ascii_uppercase
        if self.use_lowercase:
            charset += string.ascii_lowercase
        if self.use_numbers:
            charset += string.digits
        if self.use_special_chars:
            charset += string.punctuation

        if not charset:
            charset = string.ascii_letters + string.digits

        return charset

    def generate(self) -> str:
        """Gera uma nova senha aleatória.

        Returns:
            str: Senha aleatória gerada
        """
        charset = self._build_charset()
        password = "".join(random.choice(charset) for _ in range(self.length))
        return password

    def generate_multiple(self, count: int = 1) -> list:
        """Gera múltiplas senhas.

        Args:
            count: Número de senhas a gerar

        Returns:
            list: Lista de senhas geradas
        """
        return [self.generate() for _ in range(count)]

    def validate_strength(self, password: str) -> dict:
        """Valida a força de uma senha.

        Args:
            password: Senha a validar

        Returns:
            dict: Dicionário com análise de força
        """
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Senha muito curta (mínimo 8 caracteres)")

        if len(password) >= 16:
            score += 1

        if any(c.isupper() for c in password):
            score += 1
        else:
            feedback.append("Adicione letras maiúsculas")

        if any(c.islower() for c in password):
            score += 1
        else:
            feedback.append("Adicione letras minúsculas")

        if any(c.isdigit() for c in password):
            score += 1
        else:
            feedback.append("Adicione números")

        if any(c in string.punctuation for c in password):
            score += 1
        else:
            feedback.append("Adicione caracteres especiais")

        strength_levels = {
            0: "Muito Fraca",
            1: "Fraca",
            2: "Regular",
            3: "Boa",
            4: "Forte",
            5: "Muito Forte",
            6: "Excelente",
        }

        return {
            "score": score,
            "strength": strength_levels.get(score, "Excelente"),
            "feedback": feedback,
        }