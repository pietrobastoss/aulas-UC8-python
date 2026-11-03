from modelos import Produto, Item, Pedido, quantidade, formatar

def verificar():
    """
    Executa os testes automatizados para Produto, Item e Pedido sem utilizar GUI.
    Retorna True apenas se todas as asserções corretas passarem com sucesso.
    """
    print("Iniciando verificações da Aula A07 (Sorveteria)...\n")

    # 1. Criação de dados fictícios
    # Fruta a 500 centavos (R$ 5,00) e Leite a 750 centavos (R$ 7,50)
    p_fruta = Produto(101, "Fruta", 500)
    p_leite = Produto(102, "Leite", 750)

    # 2. Teste de Duas Frutas e Três Leites
    pedido = Pedido()
    pedido.adicionar(p_fruta, "2")
    pedido.adicionar(p_leite, "3")

    # Previsão: 
    # Fruta: 2 * 500 = 1000 centavos
    # Leite: 3 * 750 = 2250 centavos
    # Total: 1000 + 2250 = 3250 centavos
    assert pedido.total_centavos() == 3250, f"Erro no total esperado (esperado 3250, obtido {pedido.total_centavos()})"
    
    linhas = pedido.linhas()
    assert len(linhas) == 2, "O pedido deve conter exatamente 2 linhas de itens."
    assert linhas[0]["subtotal"] == 1000, "Subtotal da fruta incorreto."
    assert linhas[1]["subtotal"] == 2250, "Subtotal do leite incorreto."
    print("✓ Caso 1 (Duas frutas e três leites) passou com sucesso.")

    # 3. Teste de Repetição por Código
    # Adicionar mais 1 unidade da fruta (código 101) deve acumular na mesma linha (total de 3 unidades)
    pedido.adicionar(p_fruta, "1")
    
    # Previsão atualizada:
    # Fruta: 3 * 500 = 1500 centavos
    # Leite: 3 * 750 = 2250 centavos
    # Total: 1500 + 2250 = 3750 centavos
    assert pedido.total_centavos() == 3750, "Erro ao acumular quantidade com código repetido."
    assert len(pedido.linhas()) == 2, "A repetição de código não deve criar novas linhas de itens."
    assert pedido.itens[101].quantidade == 3, "A quantidade acumulada da fruta deveria ser 3."
    print("✓ Caso 2 (Repetição de código e acumulação) passou com sucesso.")

    # 4. Teste de Quantidade Inválida e Preservação de Estado
    # Captura o estado do pedido antes do erro
    total_antes_do_erro = pedido.total_centavos()
    linhas_antes_do_erro = len(pedido.linhas())

    # Tentar adicionar quantidade inválida ("abc", "0", "-2", etc.) deve levantar ValueError
    erro_capturado = False
    try:
        pedido.adicionar(p_leite, "abc")
    except ValueError:
        erro_capturado = True

    assert erro_capturado, "Deveria ter lançado ValueError para quantidade inválida ('abc')."
    
    # Prova que o pedido anterior foi preservado intacto após a exceção
    assert pedido.total_centavos() == total_antes_do_erro, "O total do pedido mudou após uma falha de validação!"
    assert len(pedido.linhas()) == linhas_antes_do_erro, "O número de itens mudou após a falha!"
    print("✓ Caso 3 (Quantidade inválida recusada e estado preservado) passou com sucesso.")

    # 5. Isolamento entre Pedidos (Pedido novo deve estar vazio)
    outro_pedido = Pedido()
    assert len(outro_pedido.linhas()) == 0, "Um segundo pedido recém-criado deve estar vazio."
    assert outro_pedido.total_centavos() == 0, "O total de um segundo pedido vazio deve ser 0."
    print("✓ Caso 4 (Isolamento de novo pedido) passou com sucesso.")

    # 6. Demonstração de Expectativa Deliberadamente Errada (conforme roteiro)
    # Testamos que uma previsão incorreta falha, e em seguida restauramos com a correta.
    esperimento_falha_capturado = False
    try:
        # Previsão incorreta propositalmente para demonstrar o comportamento do assert
        assert pedido.total_centavos() == 999999
    except AssertionError:
        esperimento_falha_capturado = True

    assert esperimento_falha_capturado, "Uma asserção falsa deve falhar obrigatoriamente."
    print("✓ Caso 5 (Expectativa falsa testada, falhou conforme previsto e o sistema foi preservado) passou com sucesso.")

    print("\nTodas as verificações foram concluídas com êxito!")
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")