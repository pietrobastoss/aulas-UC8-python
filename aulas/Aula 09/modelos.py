from decimal import Decimal, ROUND_HALF_UP

def quantidade(texto):
    """Converte e valida o texto de quantidade para um número inteiro positivo."""
    try:
        qtd = int(texto)
        if qtd <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return qtd
    except (TypeError, ValueError) as e:
        raise ValueError("Quantidade inválida.") from e

def formatar(centavos):
    """Formata um valor em centavos para o padrão monetário brasileiro (R$)."""
    reais = Decimal(centavos) / Decimal(100)
    return f"R$ {reais.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"

class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        self.codigo = int(codigo)
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
        # Usamos um dicionário onde a chave é o código do produto (garantindo identidade única)
        self._itens = {}
        self.aberto = True

    def exigir_aberto(self):
        if not self.aberto:
            raise RuntimeError("O pedido já está fechado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        qtd_adicionar = quantidade(texto_quantidade)
        
        if produto.codigo in self._itens:
            # Se o código já está no pedido, somamos à quantidade existente
            self._itens[produto.codigo].qtd += qtd_adicionar
        else:
            # Senão, criamos um novo item no dicionário associado ao código
            self._itens[produto.codigo] = Item(produto, str(qtd_adicionar))

    def atualizar(self, codigo, texto_quantidade):
        """Atualiza a quantidade de um código que já está no pedido (substitui, não soma)."""
        self.exigir_aberto()
        codigo_int = int(codigo)
        
        if codigo_int not in self._itens:
            raise KeyError(f"O produto com código {codigo_int} não está no pedido.")
            
        nova_qtd = quantidade(texto_quantidade)
        self._itens[codigo_int].qtd = nova_qtd

    def remover(self, codigo):
        """Remove inteiramente o item associado ao código do pedido."""
        self.exigir_aberto()
        codigo_int = int(codigo)
        
        if codigo_int not in self._itens:
            raise KeyError(f"O produto com código {codigo_int} não está no pedido.")
            
        del self._itens[codigo_int]

    def total_centavos(self):
        return sum(item.subtotal() for item in self._itens.values())

    def linhas(self):
        """Retorna uma lista com os dados consolidados para exibição/conferência."""
        resultado = []
        for codigo, item in self._itens.items():
            resultado.append({
                "codigo": codigo,
                "nome": item.produto.nome,
                "preco": item.produto.preco_centavos,
                "qtd": item.qtd,
                "subtotal": item.subtotal()
            })
        return resultado