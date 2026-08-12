"""Interface de linha de comando para Sabrina."""

import click
from .generator import PasswordGenerator
from .storage import PasswordStorage
from .crypto import CryptoManager


@click.group()
def cli():
    """Sabrina - Gerador de Senhas Automático"""
    pass


@cli.command()
@click.option(
    "--length",
    "-l",
    default=16,
    type=int,
    help="Comprimento da senha (padrão: 16)",
)
@click.option(
    "--uppercase/--no-uppercase",
    default=True,
    help="Incluir letras maiúsculas (padrão: sim)",
)
@click.option(
    "--lowercase/--no-lowercase",
    default=True,
    help="Incluir letras minúsculas (padrão: sim)",
)
@click.option(
    "--numbers/--no-numbers", default=True, help="Incluir números (padrão: sim)"
)
@click.option(
    "--special-chars/--no-special-chars",
    default=True,
    help="Incluir caracteres especiais (padrão: sim)",
)
@click.option(
    "--count",
    "-c",
    default=1,
    type=int,
    help="Número de senhas a gerar (padrão: 1)",
)
def generate(length, uppercase, lowercase, numbers, special_chars, count):
    """Gera uma ou mais senhas aleatórias."""
    generator = PasswordGenerator(
        length=length,
        use_uppercase=uppercase,
        use_lowercase=lowercase,
        use_numbers=numbers,
        use_special_chars=special_chars,
    )

    if count == 1:
        password = generator.generate()
        click.echo(click.style(f"🔐 Senha gerada: ", fg="blue") + click.style(password, fg="green", bold=True))
        strength = generator.validate_strength(password)
        click.echo(click.style(f"💪 Força: ", fg="blue") + click.style(strength["strength"], fg="yellow"))
    else:
        click.echo(click.style(f"🔐 Gerando {count} senhas...\n", fg="blue"))
        passwords = generator.generate_multiple(count)
        for i, password in enumerate(passwords, 1):
            click.echo(f"{i}. {click.style(password, fg='green', bold=True)}")


@cli.command()
@click.argument("service")
@click.argument("password", required=False)
@click.option(
    "--master-password",
    "-m",
    default="sabrina12345",
    prompt=False,
    help="Senha mestre",
)
def save(service, password, master_password):
    """Salva uma senha criptografada."""
    if not password:
        generator = PasswordGenerator()
        password = generator.generate()
        click.echo(click.style(f"🎲 Senha gerada: ", fg="blue") + click.style(password, fg="green", bold=True))

    storage = PasswordStorage(master_password=master_password)
    storage.save_password(service, password)
    click.echo(click.style(f"✅ Senha salva para {service}", fg="green"))


@cli.command()
@click.argument("service")
@click.option(
    "--master-password",
    "-m",
    default="sabrina12345",
    prompt=False,
    help="Senha mestre",
)
def get(service, master_password):
    """Recupera uma senha armazenada."""
    storage = PasswordStorage(master_password=master_password)
    password = storage.get_password(service)

    if password:
        click.echo(click.style(f"🔑 Senha para {service}: ", fg="blue") + click.style(password, fg="green", bold=True))
    else:
        click.echo(click.style(f"❌ Senha não encontrada para {service}", fg="red"))


@cli.command()
@click.option(
    "--master-password",
    "-m",
    default="sabrina12345",
    prompt=False,
    help="Senha mestre",
)
def list_passwords(master_password):
    """Lista todos os serviços armazenados."""
    storage = PasswordStorage(master_password=master_password)
    services = storage.list_services()

    if services:
        click.echo(click.style("📋 Serviços armazenados:\n", fg="blue"))
        for service in services:
            click.echo(f"  • {click.style(service, fg='green')}")
    else:
        click.echo(click.style("ℹ️  Nenhuma senha armazenada.", fg="yellow"))


@cli.command()
@click.argument("service")
@click.option(
    "--master-password",
    "-m",
    default="sabrina12345",
    prompt=False,
    help="Senha mestre",
)
def delete(service, master_password):
    """Deleta uma senha armazenada."""
    storage = PasswordStorage(master_password=master_password)
    if storage.delete_password(service):
        click.echo(click.style(f"✅ Senha de {service} deletada", fg="green"))
    else:
        click.echo(click.style(f"❌ Senha não encontrada para {service}", fg="red"))


@cli.command()
@click.argument("password")
def strength(password):
    """Verifica a força de uma senha."""
    generator = PasswordGenerator()
    result = generator.validate_strength(password)

    click.echo(click.style(f"🔐 Análise de Força:\n", fg="blue"))
    click.echo(f"  Pontuação: {result['score']}/6")
    click.echo(f"  Nível: {click.style(result['strength'], fg='yellow')}")

    if result["feedback"]:
        click.echo("\n  Sugestões:")
        for suggestion in result["feedback"]:
            click.echo(f"    • {suggestion}")
    else:
        click.echo("\n  " + click.style("✅ Senha muito forte!", fg="green"))


if __name__ == "__main__":
    cli()