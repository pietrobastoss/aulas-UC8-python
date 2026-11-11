# A14: assinaturas de apoio; traga sua implementação anterior.

from contextlib import closing
from pathlib import Path
import sqlite3

from pagamento import preco_para_centavos


def validar_nome(nome):
    """Valida se o nome é uma string não vazia."""
    txt = str(nome).strip() if nome is not None else ""
    if not txt:
        raise ValueError("O nome é obrigatório e não pode ser vazio.")
    return txt


def validar_id(codigo):
    """Valida e converte o código/ID para um inteiro positivo (> 0)."""
    try:
        val = int(codigo)
        if val <= 0:
            raise ValueError("O ID deve ser um número inteiro positivo.")
        return val
    except (ValueError, TypeError):
        raise ValueError("ID inválido. Informe um número inteiro positivo.")


def validar_preco(preco):
    """
    Valida e converte o texto do preço para centavos inteiros.
    Aceita inteiros (já em centavos) ou textos monetários válidos (ex: '7,50' -> 750).
    Limita o preço máximo didático a R$ 100.000,00 (10.000.000 centavos).
    """
    if isinstance(preco, int):
        centavos = preco
    else:
        centavos = preco_para_centavos(preco)

    if centavos <= 0:
        raise ValueError("O preço deve ser maior que zero.")
    if centavos > 10_000_000:
        raise ValueError("O preço excede o limite máximo permitido de R$ 100.000,00.")

    return centavos


class RepositorioSqlite:
    """Repositório de persistência de dados utilizando SQLite."""

    def __init__(self, caminho):
        if not caminho:
            raise ValueError("O caminho do banco de dados é obrigatório.")
        self.caminho = str(Path(caminho).resolve())
        self.iniciar()

    def conectar(self):
        """Retorna uma nova conexão configurada com a base de dados."""
        return sqlite3.connect(self.caminho)

    def iniciar(self):
        """Cria as tabelas 'produtos' e 'clientes' caso ainda não existam."""
        with closing(self.conectar()) as con:
            with con:
                con.execute("""
                    CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        preco_centavos INTEGER NOT NULL
                    )
                """)
                con.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL
                    )
                """)

    def adicionar_produto(self, nome, preco):
        """
        Insere um produto no banco utilizando consulta parametrizada.
        Retorna o ID gerado para a nova linha.
        """
        nome_validado = validar_nome(nome)
        preco_centavos = validar_preco(preco)

        with closing(self.conectar()) as con:
            with con:
                cursor = con.execute(
                    "INSERT INTO produtos (nome, preco_centavos) VALUES (?, ?)",
                    (nome_validado, preco_centavos)
                )
                return cursor.lastrowid

    def listar_produtos(self):
        """Retorna a lista de todos os produtos como dicionários: [{'id': ..., 'nome': ..., 'preco_centavos': ...}]."""
        with closing(self.conectar()) as con:
            cursor = con.execute("SELECT id, nome, preco_centavos FROM produtos ORDER BY id ASC")
            linhas = cursor.fetchall()
            return [
                {"id": linha[0], "nome": linha[1], "preco_centavos": linha[2]}
                for linha in linhas
            ]

    def adicionar_cliente(self, nome):
        """Insere um cliente no banco utilizando consulta parametrizada. Retorna o ID gerado."""
        nome_validado = validar_nome(nome)
        with closing(self.conectar()) as con:
            with con:
                cursor = con.execute(
                    "INSERT INTO clientes (nome) VALUES (?)",
                    (nome_validado,)
                )
                return cursor.lastrowid

    def listar_clientes(self):
        """Retorna a lista de clientes cadastrados como dicionários."""
        with closing(self.conectar()) as con:
            cursor = con.execute("SELECT id, nome FROM clientes ORDER BY id ASC")
            linhas = cursor.fetchall()
            return [
                {"id": linha[0], "nome": linha[1]}
                for linha in linhas
            ]