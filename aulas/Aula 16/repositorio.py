# A16: assinaturas de apoio; traga sua implementação anterior.

from contextlib import closing
from pathlib import Path
import sqlite3

def validar_nome(nome):
    """Valida se o nome é uma string não vazia após remoção de espaços."""
    if not isinstance(nome, str) or not nome.strip():
        raise ValueError("O nome não pode estar vazio.")
    return nome.strip()

def validar_id(codigo):
    """Valida se o ID/código corresponde a um número inteiro válido e positivo."""
    try:
        cod = int(codigo)
        if cod <= 0:
            raise ValueError("O ID deve ser maior que zero.")
        return cod
    except (ValueError, TypeError) as e:
        raise ValueError("ID inválido.") from e

def validar_preco(preco):
    """Valida e converte o preço em centavos para um inteiro positivo."""
    try:
        val = int(preco)
        if val < 0:
            raise ValueError("O preço não pode ser negativo.")
        return val
    except (ValueError, TypeError) as e:
        raise ValueError("Preço inválido.") from e

class RepositorioSqlite:

    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.iniciar()

    def conectar(self):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        return sqlite3.connect(self.caminho)

    def iniciar(self):
        """Cria as tabelas necessárias no banco SQLite se elas ainda não existirem."""
        with closing(self.conectar()) as conexao:
            with conexao:
                conexao.execute("""
                    CREATE TABLE IF NOT EXISTS produtos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        preco_centavos INTEGER NOT NULL
                    )
                """)
                conexao.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL
                    )
                """)

    def adicionar_produto(self, nome, preco):
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    "INSERT INTO produtos (nome, preco_centavos) VALUES (?, ?)",
                    (nome_valido, preco_valido)
                )
                return {"id": cursor.lastrowid, "nome": nome_valido, "preco_centavos": preco_valido}

    def listar_produtos(self):
        with closing(self.conectar()) as conexao:
            conexao.row_factory = sqlite3.Row
            cursor = conexao.execute("SELECT id, nome, preco_centavos FROM produtos ORDER BY id")
            return [
                {"id": row["id"], "nome": row["nome"], "preco_centavos": row["preco_centavos"]}
                for row in cursor.fetchall()
            ]

    def editar_produto(self, codigo, nome, preco):
        cod = validar_id(codigo)
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    "UPDATE produtos SET nome = ?, preco_centavos = ? WHERE id = ?",
                    (nome_valido, preco_valido, cod)
                )
                if cursor.rowcount == 0:
                    raise KeyError(f"Produto com ID {cod} não encontrado para edição.")
        return {"id": cod, "nome": nome_valido, "preco_centavos": preco_valido}

    def excluir_produto(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão do produto precisa ser confirmada.")
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute("DELETE FROM produtos WHERE id = ?", (cod,))
                if cursor.rowcount == 0:
                    raise KeyError(f"Produto com ID {cod} não encontrado para exclusão.")
        return True

    def adicionar_cliente(self, nome):
        nome_valido = validar_nome(nome)
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    "INSERT INTO clientes (nome) VALUES (?)",
                    (nome_valido,)
                )
                return {"id": cursor.lastrowid, "nome": nome_valido}

    def listar_clientes(self):
        with closing(self.conectar()) as conexao:
            conexao.row_factory = sqlite3.Row
            cursor = conexao.execute("SELECT id, nome FROM clientes ORDER BY id")
            return [
                {"id": row["id"], "nome": row["nome"]}
                for row in cursor.fetchall()
            ]

    def editar_cliente(self, codigo, nome):
        cod = validar_id(codigo)
        nome_valido = validar_nome(nome)
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute(
                    "UPDATE clientes SET nome = ? WHERE id = ?",
                    (nome_valido, cod)
                )
                if cursor.rowcount == 0:
                    raise KeyError(f"Cliente com ID {cod} não encontrado para edição.")
        return {"id": cod, "nome": nome_valido}

    def excluir_cliente(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão do cliente precisa ser confirmada.")
        with closing(self.conectar()) as conexao:
            with conexao:
                cursor = conexao.execute("DELETE FROM clientes WHERE id = ?", (cod,))
                if cursor.rowcount == 0:
                    raise KeyError(f"Cliente com ID {cod} não encontrado para exclusão.")
        return True