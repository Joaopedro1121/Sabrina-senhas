"""Setup do projeto Sabrina."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sabrina-password-generator",
    version="1.0.0",
    author="João Pedro",
    author_email="joaopedro@example.com",
    description="Um gerador de senhas seguro e automático com criptografia integrada",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Joaopedro1121/Sabrina-senhas",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "cryptography>=41.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "sabrina=sabrina.cli:cli",
        ],
    },
)