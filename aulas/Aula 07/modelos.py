# A07: assinaturas de apoio; traga sua implementação anterior.

def quantidade(texto):
    """
    Converte e valida a quantidade a partir de um texto.
    Deve retornar um inteiro entre 1 e 999.
    Levanta ValueError se o texto for vazio, inválido, zero, negativo ou decimal.
    """
    if texto is None:
        raise ValueError("A quantidade não pode ser vazia.")
    
    # Remove espaços em branco ao redor
    texto_limpo = str(texto).strip()
    
    if not texto_limpo:
        raise ValueError("A quantidade não pode ser vazia.")
        
    # Verifica se é estritamente um número inteiro positivo (sem sinais de + ou -, e sem ponto/vírgula)
    if not texto_limpo.isdigit():
        raise ValueError("A quantidade deve ser um número inteiro válido.")
        
    valor = int(texto_limpo)
    
    if not (1 <= valor <= 999):
        raise ValueError("A quantidade deve estar entre 1 e 999.")
        
    return valor


def formatar(centavos):
    """
    Formata um valor inteiro em centavos para o padrão de moeda em Reais (ex: 3250 -> 'R$ 32,50').
    """
    if not isinstance(centavos, (int, float)):
        raise TypeError("O valor em centavos deve ser numérico.")
    
    reais = centavos / 100
    return f"R$ {reais:.2f}".replace(".", ",")


class Produto:
    def __init__(self, codigo, nome, preco_centavos):
        """
        Guarda código, nome e preço unitário em centavos.
        """
        self.codigo = codigo
        self.nome = nome
        self.preco_centavos = int(preco_centavos)


class Item:
    def __init__(self, produto, texto_quantidade):
        """
        Relaciona um produto à quantidade escolhida (validada).
        """
        self.produto = produto
        self.quantidade = quantidade(texto_quantidade)

    def subtotal(self):
        """
        Calcula o subtotal do item em centavos (preço unitário * quantidade).
        """
        return self.produto.preco_centavos * self.quantidade


class Pedido:
    def __init__(self):
        """
        Reúne itens, garantindo uma coleção própria e isolada para cada pedido.
        Usa um dicionário onde a chave é o código do produto e o valor é o objeto Item.
        """
        self.itens = {}

    def exigir_aberto(self):
        """
        Garante que o pedido está em estado válido para receber alterações.
        """
        pass

    def adicionar(self, produto, texto_quantidade):
        """
        Adiciona um produto ao pedido ou acumula a quantidade se o código já existir.
        Valida a quantidade antes de modificar o pedido para preservar o estado anterior em caso de erro.
        """
        self.exigir_aberto()
        
        # Valida a quantidade primeiro para evitar alterações parciais/corrompidas se falhar
        qtd_nova = quantidade(texto_quantidade)
        
        # Verifica limite acumulado caso o código já exista no pedido
        if produto.codigo in self.itens:
            item_existente = self.itens[produto.codigo]
            qtd_acumulada = item_existente.quantidade + qtd_nova
            if qtd_acumulada > 999:
                raise ValueError("A quantidade total acumulada não pode ultrapassar 999.")
            item_existente.quantidade = qtd_acumulada
        else:
            # Cria um novo item se o código for inédito no pedido
            self.itens[produto.codigo] = Item(produto, texto_quantidade)

    def total_centavos(self):
        """
        Calcula o valor total do pedido somando os subtotais de todos os itens.
        """
        return sum(item.subtotal() for item in self.itens.values())

    def linhas(self):
        """
        Retorna uma lista resumida com os dados dos itens para exibição ou verificação.
        """
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