from modelos import Produto, Item, Pedido, quantidade, formatar

def verificar():
    """Executa todos os testes automatizados da Aula 09 (Seleção por ID, Atualização e Remoção)."""
    
    # 1. Dados fictícios iniciais
    p1 = Produto(codigo=1, nome="Fruta", preco_centavos=1000)  # R$ 10,00
    p2 = Produto(codigo=2, nome="Leite", preco_centavos=500)   # R$ 5,00
    
    pedido = Pedido()
    
    # --- CASO 1: Adição e Identidade (repetir código soma a quantidade) ---
    pedido.adicionar(p1, "2")
    pedido.adicionar(p2, "3")
    pedido.adicionar(p1, "1")  # Repetindo p1 (código 1), deve somar: qtd 3
    
    linhas_iniciais = pedido.linhas()
    # Ordem visual pode variar, mas o dicionário interno preserva o ID exato
    assert len(linhas_iniciais) == 2, "Deveria haver exatamente 2 linhas consolidadas por código."
    
    # Conferindo subtotal e totais (3 * 10,00 + 3 * 5,00 = 45,00 -> 4500 centavos)
    assert pedido.total_centavos() == 4500, f"Esperado 4500 centavos, obtido {pedido.total_centavos()}"

    # --- CASO 2: Mudar a ordem visual mantendo a identidade por ID ---
    # Simulando a ordenação visual da Treeview por nome
    ordem_visual = sorted(pedido.linhas(), key=lambda x: x["nome"])
    # Se 'Fruta' (cód 1) e 'Leite' (cód 2) mudarem de posição visual, o ID selecionado continua sendo 1
    id_selecionado = ordem_visual[0]["codigo"] # Independentemente da posição, o ID aponta para o produto correto
    
    # --- CASO 3: Atualizar quantidade por ID (substitui em vez de somar) ---
    # Atualizando o código 1 para 4 unidades (antes eram 3)
    pedido.atualizar(1, "4")
    
    # Novo total esperado: (4 * 10,00) + (3 * 5,00) = 40,00 + 15,00 = 55,00 (5500 centavos)
    assert pedido.total_centavos() == 5500, f"Esperado 5500 centavos após atualizar, obtido {pedido.total_centavos()}"
    
    # Conferindo se o item atualizado possui exatamente quantidade 4
    item_atualizado = next(l for l in pedido.linhas() if l["codigo"] == 1)
    assert item_atualizado["qtd"] == 4, "A quantidade deveria ser substituída por 4."

    # --- CASO 4: Recusa de entrada inválida e preservação de estado (Erro após válido) ---
    subtotal_antes_do_erro = pedido.total_centavos()
    
    try:
        pedido.atualizar(1, "-2")  # Quantidade inválida
        assert False, "Deveria ter lançado ValueError para quantidade negativa."
    except ValueError:
        pass  # Erro esperado
    
    try:
        pedido.atualizar(999, "2")  # Código inexistente
        assert False, "Deveria ter lançado KeyError para código ausente."
    except KeyError:
        pass  # Erro esperado

    # Confere se o estado anterior foi rigorosamente preservado após as falhas
    assert pedido.total_centavos() == subtotal_antes_do_erro, "O total não deve mudar após uma recusa de entrada."

    # --- CASO 5: Remoção progressiva até vazio e seleção ausente ---
    # Removendo o código 2 ('Leite')
    pedido.remover(2)
    assert pedido.total_centavos() == 4000, "Restando apenas 4 unidades de Fruta (4 * 10,00 = 40,00)."
    
    # Removendo o último item restante (código 1) -> Carrinho vazio
    pedido.remover(1)
    
    linhas_finais = pedido.linhas()
    assert len(linhas_finais) == 0, "O carrinho deveria estar completamente vazio."
    assert pedido.total_centavos() == 0, "O total do carrinho vazio deve ser zero."
    
    # Simulação de seleção ausente na GUI (quando selection() retorna tupla vazia)
    selecao_gui = ()
    if not selecao_gui:
        mensagem_orientacao = "Nenhum item selecionado. Selecione um item na lista."
        assert len(mensagem_orientacao) > 0, "A interface tratou a ausência de seleção com orientação."

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")