# A08: modelos.py — Sorveteria
from decimal import Decimal

def quantidade(texto):
    """Converte e valida texto de quantidade (inteiro positivo)."""
    try:
        val = int(str(texto).strip())
        if val <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")
        return val
    except Exception as e:
        raise ValueError(f"Quantidade inválida: {e}")

def formatar(centavos):
    """Formata centavos em string monetária R$ X,XX."""
    reais = centavos / 100
    return f"R$ {reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = str(codigo)
        self.nome = str(nome)
        self.preco_centavos = int(preco_centavos)

class Item:
    def __init__(self, produto, texto_quantidade):
        self.produto = produto
        self.qtd = quantidade(texto_quantidade)

    def subtotal(self):
        return self.produto.preco_centavos * self.qtd

class Pedido:
    def __init__(self):
        self.itens = []
        self._aberto = True

    def exigir_aberto(self):
        if not self._aberto:
            raise RuntimeError("Pedido fechado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        item = Item(produto, texto_quantidade)
        self.itens.append(item)

    def total_centavos(self):
        return sum(item.subtotal() for item in self.itens)

    def linhas(self):
        return [(item.produto.codigo, item.produto.nome, item.qtd, item.subtotal()) for item in self.itens]