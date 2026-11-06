# A12: assinaturas de apoio; implementação completa do modelo de dados.

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

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
    """Formata um valor inteiro em centavos para a representação em moeda (ex: R$ 10,50)."""
    try:
        valor = Decimal(int(centavos)) / Decimal(100)
        valor = valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # Formato brasileiro: milhar com ponto e decimal com vírgula (ex: R$ 1.234,50)
        texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {texto}"
    except (ValueError, TypeError, InvalidOperation):
        return "R$ 0,00"


class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = int(codigo)
        self.nome = str(nome).strip()
        self.preco_centavos = int(preco_centavos)  # Garante que guarda o valor inteiro em centavos
        if self.preco_centavos < 0:
            raise ValueError("O preço em centavos não pode ser negativo.")


class Item:
    def __init__(self, produto, texto_quantidade):
        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        return self.produto.preco_centavos * self.quantidade


class Pedido:
    def __init__(self):
        self._itens = {}  # Mapeia codigo_produto -> Item
        self._aberto = True
        self._forma_pagamento = None
        self._confirmado = False

    def exigir_aberto(self):
        if not self._aberto:
            raise RuntimeError("O pedido já foi finalizado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        qtd = quantidade(texto_quantidade)
        codigo = produto.codigo
        if codigo in self._itens:
            self._itens[codigo].quantidade += qtd
        else:
            self._itens[codigo] = Item(produto, qtd)

    def total_centavos(self):
        return sum(item.subtotal() for item in self._itens.values())

    def linhas(self):
        resultado = []
        for item in self._itens.values():
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
        if cod not in self._itens:
            raise KeyError("Item não encontrado no pedido.")
        qtd = quantidade(texto_quantidade)
        self._itens[cod].quantidade = qtd

    def remover(self, codigo):
        self.exigir_aberto()
        cod = int(codigo)
        if cod in self._itens:
            del self._itens[cod]

    def finalizar(self, forma, confirmado):
        self.exigir_aberto()
        if not self._itens:
            raise ValueError("Não é possível finalizar um pedido vazio.")
        self._forma_pagamento = str(forma).strip()
        self._confirmado = bool(confirmado)
        if self._confirmado:
            self._aberto = False

    def novo(self):
        self._itens.clear()
        self._aberto = True
        self._forma_pagamento = None
        self._confirmado = False