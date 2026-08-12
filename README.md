# 🔐 Sabrina - Gerador de Senhas Automático

Um gerador de senhas seguro e automático com criptografia integrada. Gere senhas fortes e armazene-as com segurança usando a senha mestre.

## ✨ Funcionalidades

- ✅ Geração de senhas aleatórias e seguras
- ✅ Opções personalizáveis (comprimento, caracteres especiais, números, letras maiúsculas/minúsculas)
- ✅ Criptografia com senha mestre "sabrina12345"
- ✅ Armazenamento seguro de senhas
- ✅ Interface CLI intuitiva
- ✅ Testes automatizados

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/Joaopedro1121/Sabrina-senhas.git
cd Sabrina-senhas

# Instale as dependências
pip install -r requirements.txt
```

## 💻 Uso

### Gerar uma Senha

```bash
python -m sabrina generate
```

### Gerar com Opções Personalizadas

```bash
# Senha com 32 caracteres
python -m sabrina generate --length 32

# Incluir caracteres especiais
python -m sabrina generate --special-chars

# Apenas maiúsculas e números
python -m sabrina generate --uppercase --numbers --no-lowercase
```

### Salvar uma Senha (Criptografada)

```bash
python -m sabrina save "meu-site.com" "senha-gerada"
```

### Recuperar uma Senha

```bash
python -m sabrina get "meu-site.com"
```

### Listar Todas as Senhas

```bash
python -m sabrina list
```

## 🔒 Segurança

- Todas as senhas são criptografadas com AES-256
- Usa a senha mestre: `sabrina12345`
- Armazenamento local seguro
- Nunca compartilhe a senha mestre!

## 📝 Estrutura do Projeto

```
Sabrina-senhas/
├── sabrina/
│   ├── __init__.py
│   ├── generator.py          # Gerador de senhas
│   ├── crypto.py             # Sistema de criptografia
│   ├── storage.py            # Gerenciamento de armazenamento
│   └── cli.py                # Interface de linha de comando
├── tests/
│   ├── test_generator.py
│   ├── test_crypto.py
│   └── test_storage.py
├── requirements.txt
├── setup.py
└── README.md
```

## 🧪 Testes

```bash
pytest tests/ -v
```

## 📄 Licença

MIT License - Veja LICENSE para mais detalhes

## 👨‍💻 Autor

Criado por João Pedro - [Joaopedro1121](https://github.com/Joaopedro1121)