# A16: assinaturas de apoio; traga sua implementação anterior.
from decimal import Decimal, ROUND_HALF_UP

def quantidade(texto):
    """Converte e valida o texto da quantidade para um número inteiro positivo."""
    try:
        qtd = int(str(texto).strip())
        if qtd <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return qtd
    except (ValueError, TypeError) as e:
        raise ValueError("Quantidade inválida.") from e

def formatar(centavos):
    """Formata um valor em centavos para o padrão monetário brasileiro (R$ X,XX)."""
    try:
        valor = Decimal(centavos) / Decimal(100)
        return f"R$ {valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):_}".replace('.', ',').replace('_', '.')
    except Exception as e:
        raise ValueError("Erro ao formatar valor monetário.") from e

class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = int(codigo)
        self.nome = str(nome).strip()
        self.preco_centavos = int(preco_centavos)

class Item:
    def __init__(self, produto, texto_quantidade):
        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        return self.produto.preco_centavos * self.quantidade

class Pedido:
    def __init__(self):
        self.itens = {}  # Mapeia código do produto -> Item
        self.status = "aberto"  # "aberto" ou "finalizado"

    def exigir_aberto(self):
        if self.status != "aberto":
            raise RuntimeError("O pedido já foi finalizado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        qtd = quantidade(texto_quantidade)
        if produto.codigo in self.itens:
            self.itens[produto.codigo].quantidade += qtd
        else:
            self.itens[produto.codigo] = Item(produto, qtd)

    def total_centavos(self):
        return sum(item.subtotal() for item in self.itens.values())

    def linhas(self):
        """Retorna uma lista resumida das linhas do pedido para relatórios/exibição."""
        resultado = []
        for item in self.itens.values():
            resultado.append({
                "codigo": item.produto.codigo,
                "nome": item.produto.nome,
                "preco_unitario": item.produto.preco_centavos,
                "quantidade": item.quantidade,
                "subtotal": item.subtotal()
            })
        return resultado

    def atualizar(self, codigo, texto_quantidade):
        self.exigir_aberto()
        cod = int(codigo)
        if cod not in self.itens:
            raise KeyError("Item não encontrado no pedido.")
        qtd = quantidade(texto_quantidade)
        self.itens[cod].quantidade = qtd

    def remover(self, codigo):
        self.exigir_aberto()
        cod = int(codigo)
        if cod in self.itens:
            del self.itens[cod]

    def finalizar(self, forma, confirmado):
        self.exigir_aberto()
        if not confirmado:
            raise ValueError("O pagamento precisa estar confirmado para finalizar o pedido.")
        if not self.itens:
            raise ValueError("Não é possível finalizar um pedido vazio.")
        self.status = "finalizado"
        return {
            "forma": forma,
            "total_centavos": self.total_centavos(),
            "itens": self.linhas()
        }

    def novo(self):
        self.itens.clear()
        self.status = "aberto"