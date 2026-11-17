# A17: assinaturas de apoio; traga sua implementação anterior.

from contextlib import closing
from pathlib import Path
import sqlite3

def validar_nome(nome):
    """Valida se o nome informado é uma string não vazia."""
    if nome is None:
        raise ValueError("O nome não pode ser nulo.")
    limpo = str(nome).strip()
    if not limpo:
        raise ValueError("O nome não pode estar vazio.")
    return limpo

def validar_id(codigo):
    """Valida e converte um código/ID para inteiro positivo."""
    try:
        cod = int(codigo)
        if cod <= 0:
            raise ValueError("O ID deve ser um número positivo.")
        return cod
    except (ValueError, TypeError) as e:
        raise ValueError("ID inválido.") from e

def validar_preco(preco):
    """Valida e converte o preço para inteiro em centavos positivo ou zero."""
    try:
        p = int(preco)
        if p < 0:
            raise ValueError("O preço não pode ser negativo.")
        return p
    except (ValueError, TypeError) as e:
        raise ValueError("Preço inválido.") from e

class RepositorioSqlite:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.iniciar()

    def conectar(self):
        """Cria e retorna uma conexão SQLite com chaves estrangeiras habilitadas."""
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(self.caminho)
        con.execute("PRAGMA foreign_keys = ON;")
        con.row_factory = sqlite3.Row
        return con

    def iniciar(self):
        """Cria as tabelas estruturais necessárias para produtos, clientes, vendas e itens de venda."""
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
                # Tabela de Vendas / Cabeçalho do Pedido
                con.execute("""
                    CREATE TABLE IF NOT EXISTS vendas (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cliente_id INTEGER NOT NULL,
                        forma_pagamento TEXT NOT NULL,
                        total_centavos INTEGER NOT NULL,
                        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
                    )
                """)
                # Tabela de Itens da Venda (retratos de preço e quantidade vinculados à venda)
                con.execute("""
                    CREATE TABLE IF NOT EXISTS itens_venda (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        venda_id INTEGER NOT NULL,
                        produto_id INTEGER NOT NULL,
                        nome_produto TEXT NOT NULL,
                        preco_unitario INTEGER NOT NULL,
                        quantidade INTEGER NOT NULL,
                        subtotal INTEGER NOT NULL,
                        FOREIGN KEY (venda_id) REFERENCES vendas(id) ON DELETE CASCADE,
                        FOREIGN KEY (produto_id) REFERENCES produtos(id)
                    )
                """)

    def adicionar_produto(self, nome, preco):
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        with closing(self.conectar()) as con:
            with con:
                cursor = con.execute(
                    "INSERT INTO produtos (nome, preco_centavos) VALUES (?, ?)",
                    (nome_valido, preco_valido)
                )
                return cursor.lastrowid

    def listar_produtos(self):
        with closing(self.conectar()) as con:
            cursor = con.execute("SELECT id, nome, preco_centavos FROM produtos ORDER BY id")
            return [dict(row) for row in cursor.fetchall()]

    def adicionar_cliente(self, nome):
        nome_valido = validar_nome(nome)
        with closing(self.conectar()) as con:
            with con:
                cursor = con.execute(
                    "INSERT INTO clientes (nome) VALUES (?)",
                    (nome_valido,)
                )
                return cursor.lastrowid

    def listar_clientes(self):
        with closing(self.conectar()) as con:
            cursor = con.execute("SELECT id, nome FROM clientes ORDER BY id")
            return [dict(row) for row in cursor.fetchall()]

    def editar_produto(self, codigo, nome, preco):
        cod = validar_id(codigo)
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        with closing(self.conectar()) as con:
            with con:
                cursor = con.execute(
                    "UPDATE produtos SET nome = ?, preco_centavos = ? WHERE id = ?",
                    (nome_valido, preco_valido, cod)
                )
                if cursor.rowcount == 0:
                    raise KeyError(f"Produto com ID {cod} não encontrado.")
        return True

    def excluir_produto(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão precisa ser confirmada explicitamente.")
        with closing(self.conectar()) as con:
            with con:
                try:
                    cursor = con.execute("DELETE FROM produtos WHERE id = ?", (cod,))
                    if cursor.rowcount == 0:
                        raise KeyError(f"Produto com ID {cod} não encontrado.")
                except sqlite3.IntegrityError as e:
                    raise RuntimeError("Não é possível excluir um produto vinculado a vendas registradas.") from e
        return True

    def editar_cliente(self, codigo, nome):
        cod = validar_id(codigo)
        nome_valido = validar_nome(nome)
        with closing(self.conectar()) as con:
            with con:
                cursor = con.execute(
                    "UPDATE clientes SET nome = ? WHERE id = ?",
                    (nome_valido, cod)
                )
                if cursor.rowcount == 0:
                    raise KeyError(f"Cliente com ID {cod} não encontrado.")
        return True

    def excluir_cliente(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão precisa ser confirmada explicitamente.")
        with closing(self.conectar()) as con:
            with con:
                try:
                    cursor = con.execute("DELETE FROM clientes WHERE id = ?", (cod,))
                    if cursor.rowcount == 0:
                        raise KeyError(f"Cliente com ID {cod} não encontrado.")
                except sqlite3.IntegrityError as e:
                    raise RuntimeError("Não é possível excluir um cliente vinculado a vendas registradas.") from e
        return True

    def iniciar_vendas(self):
        """Método de suporte/compatibilidade para inicializar estruturas de venda se necessário."""
        self.iniciar()

    def registrar_venda(self, cliente_id, itens, forma):
        """Registra a venda e todos os seus itens estritamente dentro da mesma transação.
        Garante rollback automático em caso de qualquer falha (evitando vendas parciais).
        """
        cli_id = validar_id(cliente_id)
        if not itens or not isinstance(itens, list):
            raise ValueError("O pedido deve conter ao menos um item válido.")
        
        # Validação prévia de formato dos itens
        for item in itens:
            if not isinstance(item, dict):
                raise ValueError("Estrutura de item inválida.")
            validar_id(item.get("codigo"))
            validar_preco(item.get("subtotal", 0))

        with closing(self.conectar()) as con:
            # Inicia o bloco de transação (context manager do sqlite3 cuida do commit ou rollback)
            with con:
                # Verifica se o cliente existe
                cli_check = con.execute("SELECT id FROM clientes WHERE id = ?", (cli_id,)).fetchone()
                if not cli_check:
                    raise ValueError(f"Cliente ID {cli_id} não cadastrado.")

                # Calcula o total geral da venda em centavos a partir dos itens
                total_geral = sum(int(item["subtotal"]) for item in itens)

                # Insere o cabeçalho da venda
                cursor_venda = con.execute(
                    "INSERT INTO vendas (cliente_id, forma_pagamento, total_centavos) VALUES (?, ?, ?)",
                    (cli_id, forma, total_geral)
                )
                venda_id = cursor_venda.lastrowid

                # Insere cada item vinculado à venda na mesma transação
                for item in itens:
                    prod_id = validar_id(item.get("codigo"))
                    nome_prod = validar_nome(item.get("nome"))
                    preco_unit = validar_preco(item.get("preco_unitario"))
                    qtd = int(item.get("quantidade", 0))
                    subtotal_item = validar_preco(item.get("subtotal"))

                    if qtd <= 0:
                        raise ValueError("A quantidade do item deve ser maior que zero.")

                    con.execute(
                        """
                        INSERT INTO itens_venda (venda_id, produto_id, nome_produto, preco_unitario, quantidade, subtotal)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (venda_id, prod_id, nome_prod, preco_unit, qtd, subtotal_item)
                    )

                return venda_id

    def listar_vendas(self):
        """Retorna a listagem de vendas registradas com seus respectivos itens."""
        with closing(self.conectar()) as con:
            vendas_cursor = con.execute("""
                SELECT v.id, v.cliente_id, c.nome as cliente_nome, v.forma_pagamento, v.total_centavos
                FROM vendas v
                JOIN clientes c ON v.cliente_id = c.id
                ORDER BY v.id
            """)
            vendas = []
            for row in vendas_cursor.fetchall():
                venda_dict = dict(row)
                itens_cursor = con.execute("""
                    SELECT produto_id as codigo, nome_produto as nome, preco_unitario, quantidade, subtotal
                    FROM itens_venda WHERE venda_id = ?
                """, (venda_dict["id"],))
                venda_dict["itens"] = [dict(i) for i in itens_cursor.fetchall()]
                vendas.append(venda_dict)
            return vendas