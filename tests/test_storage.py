"""Testes para o gerenciador de armazenamento."""

import pytest
import tempfile
from pathlib import Path
from sabrina.storage import PasswordStorage


@pytest.fixture
def temp_storage():
    """Cria um armazenamento temporário para testes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage_file = Path(tmpdir) / "passwords.json"
        yield PasswordStorage(storage_file=str(storage_file))


def test_save_and_get_password(temp_storage):
    """Testa salvar e recuperar uma senha."""
    temp_storage.save_password("github", "minha_senha123")
    password = temp_storage.get_password("github")
    assert password == "minha_senha123"


def test_get_nonexistent_password(temp_storage):
    """Testa recuperar senha que não existe."""
    password = temp_storage.get_password("inexistente")
    assert password is None


def test_list_services(temp_storage):
    """Testa listar serviços."""
    temp_storage.save_password("github", "senha1")
    temp_storage.save_password("gmail", "senha2")
    temp_storage.save_password("twitter", "senha3")

    services = temp_storage.list_services()
    assert len(services) == 3
    assert "github" in services
    assert "gmail" in services
    assert "twitter" in services


def test_delete_password(temp_storage):
    """Testa deletar uma senha."""
    temp_storage.save_password("github", "senha")
    assert temp_storage.delete_password("github") is True
    assert temp_storage.get_password("github") is None


def test_delete_nonexistent_password(temp_storage):
    """Testa deletar senha que não existe."""
    assert temp_storage.delete_password("inexistente") is False


def test_update_password(temp_storage):
    """Testa atualizar uma senha."""
    temp_storage.save_password("github", "senha_antiga")
    assert temp_storage.update_password("github", "senha_nova") is True
    assert temp_storage.get_password("github") == "senha_nova"


def test_update_nonexistent_password(temp_storage):
    """Testa atualizar senha que não existe."""
    assert temp_storage.update_password("inexistente", "nova_senha") is False