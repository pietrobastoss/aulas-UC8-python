# A17: assinaturas de apoio; traga sua implementação anterior.

from decimal import Decimal, ROUND_HALF_UP

def quantidade(texto):
    """Valida e converte uma string de quantidade para um número inteiro positivo."""
    if texto is None:
        raise ValueError("A quantidade não pode ser nula.")
    
    limpo = str(texto).strip()
    if not limpo:
        raise ValueError("O campo de quantidade está vazio.")
    
    try:
        qtd = int(limpo)
        if qtd <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return qtd
    except (ValueError, TypeError) as e:
        raise ValueError("Quantidade inválida.") from e

def formatar(centavos):
    """Formata um valor inteiro em centavos para uma string monetária amigável em Reais (R$)."""
    try:
        val = int(centavos)
    except (ValueError, TypeError) as e:
        raise ValueError("Valor em centavos inválido.") from e
        
    decimal_valor = Decimal(val) / Decimal(100)
    # Formata com duas casas decimais e substitui o ponto da casa decimal por vírgula
    texto_formatado = f"{decimal_valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"
    texto_pt = texto_formatado.replace('.', ',')
    return f"R$ {texto_pt}"

class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = int(codigo)
        self.nome = str(nome).strip()
        self.preco_centavos = int(preco_centavos)
        
        if not self.nome:
            raise ValueError("O nome do produto não pode estar vazio.")
        if self.preco_centavos < 0:
            raise ValueError("O preço do produto não pode ser negativo.")

class Item:
    def __init__(self, produto, texto_quantidade):
        if not isinstance(produto, Produto):
            raise TypeError("O item precisa estar associado a um objeto Produto válido.")
        self.produto = produto
        self.qtd = quantidade(texto_quantidade)

    def subtotal(self):
        """Calcula o subtotal em centavos para este item (preço unitário x quantidade)."""
        return self.produto.preco_centavos * self.qtd

class Pedido:
    def __init__(self):
        self.itens = {}  # Mapeia codigo_produto -> Item
        self.estado = "ABERTO"  # "ABERTO" ou "FINALIZADO"
        self._comprovante_final = None

    def exigir_aberto(self):
        if self.estado != "ABERTO":
            raise RuntimeError("O pedido já foi finalizado e não pode ser alterado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        codigo = produto.codigo
        
        if codigo in self.itens:
            # Se já existe, atualiza a quantidade somando ou ajustando
            item_existente = self.itens[codigo]
            nova_qtd = item_existente.qtd + quantidade(texto_quantidade)
            item_existente.qtd = nova_qtd
        else:
            self.itens[codigo] = Item(produto, texto_quantidade)

    def total_centavos(self):
        """Retorna a soma de todos os subtotais dos itens do pedido em centavos."""
        return sum(item.subtotal() for item in self.itens.values())

    def linhas(self):
        """Retorna uma lista resumida com os dados de cada linha da montagem atual."""
        resultado = []
        for codigo, item in sorted(self.itens.items()):
            resultado.append({
                "codigo": codigo,
                "nome": item.produto.nome,
                "preco_unitario": item.produto.preco_centavos,
                "quantidade": item.qtd,
                "subtotal": item.subtotal()
            })
        return resultado

    def atualizar(self, codigo, texto_quantidade):
        self.exigir_aberto()
        cod = int(codigo)
        if cod not in self.itens:
            raise KeyError(f"Produto com código {cod} não encontrado no pedido.")
        
        nova_qtd = quantidade(texto_quantidade)
        self.itens[cod].qtd = nova_qtd

    def remover(self, codigo):
        self.exigir_aberto()
        cod = int(codigo)
        if cod not in self.itens:
            raise KeyError(f"Produto com código {cod} não encontrado no pedido.")
        del self.itens[cod]

    def finalizar(self, forma, confirmado):
        self.exigir_aberto()
        if not self.itens:
            raise ValueError("Não é possível finalizar um pedido vazio.")
        if not confirmado:
            raise ValueError("A finalização do pedido precisa ser confirmada.")

        from pagamento import calcular_pagamento
        
        subtotal_centavos = self.total_centavos()
        subtotal_str = str(Decimal(subtotal_centavos) / Decimal(100))
        
        res_pagamento = calcular_pagamento(subtotal_str, forma)
        
        self._comprovante_final = {
            "itens": self.linhas(),
            "subtotal_centavos": subtotal_centavos,
            "forma": forma,
            "fator": str(res_pagamento["fator"]),
            "total_centavos": int((res_pagamento["total"] * Decimal(100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)),
            "total_formatado": formatar(int((res_pagamento["total"] * Decimal(100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)))
        }
        
        self.estado = "FINALIZADO"
        return self._comprovante_final

    def novo(self):
        """Reseta o pedido para um novo ciclo de montagem."""
        self.itens.clear()
        self.estado = "ABERTO"
        self._comprovante_final = None