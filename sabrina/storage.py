"""Módulo de armazenamento seguro de senhas."""

import json
import os
from pathlib import Path
from typing import Dict, Optional
from .crypto import CryptoManager


class PasswordStorage:
    """Gerencia armazenamento seguro de senhas."""

    def __init__(
        self,
        storage_file: str = "~/.sabrina/passwords.json",
        master_password: str = "sabrina12345",
    ):
        """
        Inicializa o gerenciador de armazenamento.

        Args:
            storage_file: Caminho do arquivo de armazenamento
            master_password: Senha mestre para criptografia
        """
        self.storage_path = Path(storage_file).expanduser()
        self.crypto = CryptoManager(master_password)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Garante que o diretório de armazenamento existe."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self.storage_path.write_text(json.dumps({}))

    def _load_data(self) -> Dict:
        """Carrega dados do arquivo de armazenamento."""
        try:
            return json.loads(self.storage_path.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_data(self, data: Dict) -> None:
        """Salva dados no arquivo de armazenamento."""
        self._ensure_storage_exists()
        self.storage_path.write_text(json.dumps(data, indent=2))

    def save_password(self, service: str, password: str) -> None:
        """Salva uma senha criptografada.

        Args:
            service: Nome do serviço/site
            password: Senha a salvar
        """
        data = self._load_data()
        encrypted_password = self.crypto.encrypt(password)
        data[service] = {
            "password": encrypted_password,
            "service": service,
        }
        self._save_data(data)

    def get_password(self, service: str) -> Optional[str]:
        """Recupera uma senha descriptografada.

        Args:
            service: Nome do serviço/site

        Returns:
            str: Senha descriptografada ou None se não encontrada
        """
        data = self._load_data()
        if service not in data:
            return None

        try:
            encrypted_password = data[service]["password"]
            return self.crypto.decrypt(encrypted_password)
        except ValueError as e:
            raise ValueError(f"Erro ao recuperar senha para {service}: {e}")

    def list_services(self) -> list:
        """Lista todos os serviços armazenados.

        Returns:
            list: Lista de nomes de serviços
        """
        data = self._load_data()
        return list(data.keys())

    def delete_password(self, service: str) -> bool:
        """Deleta uma senha armazenada.

        Args:
            service: Nome do serviço/site

        Returns:
            bool: True se deletado com sucesso, False se não encontrado
        """
        data = self._load_data()
        if service in data:
            del data[service]
            self._save_data(data)
            return True
        return False

    def update_password(self, service: str, new_password: str) -> bool:
        """Atualiza uma senha armazenada.

        Args:
            service: Nome do serviço/site
            new_password: Nova senha

        Returns:
            bool: True se atualizado com sucesso
        """
        if service in self._load_data():
            self.save_password(service, new_password)
            return True
        return False