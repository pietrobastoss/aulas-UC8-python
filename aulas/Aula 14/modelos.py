# A14: assinaturas de apoio; traga sua implementação anterior.

def quantidade(texto):
    """Converte e valida o texto de quantidade para inteiro positivo (> 0)."""
    try:
        val = int(str(texto).strip())
        if val <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        return val
    except (ValueError, TypeError):
        raise ValueError("Quantidade inválida. Informe um número inteiro positivo.")


def formatar(centavos):
    """Formata valor em centavos (inteiro) para string no padrão monetário brasileiro (ex: R$ 12,50)."""
    if not isinstance(centavos, int):
        try:
            centavos = int(centavos)
        except (ValueError, TypeError):
            raise ValueError("Valor em centavos deve ser numérico.")
    reais = centavos / 100
    return f"R$ {reais:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        if not str(codigo).strip():
            raise ValueError("Código do produto é obrigatório.")
        if not str(nome).strip():
            raise ValueError("Nome do produto é obrigatório.")
        if not isinstance(preco_centavos, int) or preco_centavos < 0:
            raise ValueError("Preço em centavos deve ser um inteiro não negativo.")
            
        self.codigo = str(codigo).strip()
        self.nome = str(nome).strip()
        self.preco_centavos = preco_centavos


class Pizza(Produto):
    def __init__(self, codigo, nome, tamanho, preco_centavos):
        super().__init__(codigo, nome, preco_centavos)
        if not str(tamanho).strip():
            raise ValueError("Tamanho é obrigatório.")
        self.tamanho = str(tamanho).strip()


class Bebida(Produto):
    def __init__(self, codigo, nome, preco_centavos):
        super().__init__(codigo, nome, preco_centavos)


class Item:
    def __init__(self, produto, texto_quantidade):
        if not isinstance(produto, Produto):
            raise ValueError("Objeto produto inválido.")
        self.produto = produto
        self.qtd = quantidade(texto_quantidade)

    def subtotal(self):
        """Retorna o subtotal do item em centavos."""
        return self.produto.preco_centavos * self.qtd


class Pedido:
    def __init__(self):
        self.itens = {}  # Mapeia codigo_produto -> Instância de Item
        self.status = "ABERTO"  # Estados: ABERTO, FINALIZADO
        self.comprovante = None

    def exigir_aberto(self):
        """Garante que operações de modificação só ocorram em pedidos abertos."""
        if self.status != "ABERTO":
            raise ValueError("Operação não permitida: o pedido já foi finalizado.")

    def adicionar(self, produto, texto_quantidade):
        self.exigir_aberto()
        qtd_valida = quantidade(texto_quantidade)
        cod = produto.codigo
        
        if cod in self.itens:
            nova_qtd = self.itens[cod].qtd + qtd_valida
            self.itens[cod] = Item(produto, nova_qtd)
        else:
            self.itens[cod] = Item(produto, qtd_valida)

    def total_centavos(self):
        """Calcula a soma de todos os subtotais dos itens do pedido."""
        return sum(item.subtotal() for item in self.itens.values())

    def linhas(self):
        """Retorna a lista com a representação tabular ou estruturada dos itens."""
        resultado = []
        for item in self.itens.values():
            resultado.append({
                "codigo": item.produto.codigo,
                "nome": item.produto.nome,
                "quantidade": item.qtd,
                "preco_unitario": item.produto.preco_centavos,
                "subtotal": item.subtotal()
            })
        return resultado

    def atualizar(self, codigo, texto_quantidade):
        self.exigir_aberto()
        cod = str(codigo).strip()
        if cod not in self.itens:
            raise ValueError(f"Item com código '{cod}' não encontrado no pedido.")
        qtd_valida = quantidade(texto_quantidade)
        produto = self.itens[cod].produto
        self.itens[cod] = Item(produto, qtd_valida)

    def remover(self, codigo):
        self.exigir_aberto()
        cod = str(codigo).strip()
        if cod not in self.itens:
            raise ValueError(f"Item com código '{cod}' não encontrado no pedido.")
        del self.itens[cod]

    def finalizar(self, forma, confirmado=True):
        """
        Finaliza o pedido se houver itens e gera o comprovante.
        Preserva a estrutura do comprovante para consumo por relatorios.py.
        """
        self.exigir_aberto()
        if not self.itens:
            raise ValueError("Não é possível finalizar um pedido vazio.")
        if not confirmado:
            raise ValueError("A confirmação do pagamento é necessária.")

        self.status = "FINALIZADO"
        total = self.total_centavos()
        
        self.comprovante = {
            "forma_pagamento": forma,
            "total_centavos": total,
            "total_formatado": formatar(total),
            "itens": [
                {
                    "codigo": item.produto.codigo,
                    "nome": item.produto.nome,
                    "quantidade": item.qtd,
                    "preco_unitario_centavos": item.produto.preco_centavos,
                    "subtotal_centavos": item.subtotal()
                }
                for item in self.itens.values()
            ]
        }
        return self.comprovante

    def novo(self):
        """Reinicia a instância do pedido para um novo ciclo de compra."""
        self.itens = {}
        self.status = "ABERTO"
        self.comprovante = None