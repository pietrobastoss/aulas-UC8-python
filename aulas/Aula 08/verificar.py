# A08: verificar.py — Sorveteria
from decimal import Decimal
from pagamento import calcular_pagamento, valor_monetario
from modelos import Produto, Pedido

def verificar():
    # 1. Testar R$ 100,00 nas quatro formas
    sub_100 = "100.00"
    
    # Dinheiro: 87.00
    sub, desc, tot = calcular_pagamento(sub_100, "Dinheiro")
    assert sub == Decimal("100.00")
    assert tot == Decimal("87.00")
    assert desc == Decimal("13.00")

    # PIX: 87.00
    sub, desc, tot = calcular_pagamento(sub_100, "PIX")
    assert tot == Decimal("87.00")

    # Débito: 92.00
    sub, desc, tot = calcular_pagamento(sub_100, "Débito")
    assert tot == Decimal("92.00")

    # Crédito 1x: 100.00
    sub, desc, tot = calcular_pagamento(sub_100, "Crédito 1x")
    assert tot == Decimal("100.00")

    # 2. Testar PIX sobre 0,50 -> total arredondado 0,44 (0.50 * 0.87 = 0.435 -> 0.44 com HALF_UP)
    sub_050 = "0.50"
    sub, desc, tot = calcular_pagamento(sub_050, "PIX")
    assert tot == Decimal("0.44")
    assert sub == Decimal("0.50")
    assert desc == Decimal("0.06")

    # 3. Repetição da chamada (sem desconto acumulado)
    res1 = calcular_pagamento("100.00", "PIX")
    res2 = calcular_pagamento("100.00", "PIX")
    assert res1 == res2, "Repetição da chamada deve produzir exatamente o mesmo resultado."

    # 4. Testar integração com Pedido (garantir que itens não são alterados)
    p = Pedido()
    prod = Produto("01", "Sorvete", 10000) # R$ 100,00 em centavos
    p.adicionar(prod, "1")
    
    sub_pedido_texto = f"{p.total_centavos() / 100:.2f}"
    sub_p, desc_p, tot_p = calcular_pagamento(sub_pedido_texto, "PIX")
    assert p.total_centavos() == 10000, "O pedido não deve ter seus centavos alterados pelo cálculo de pagamento."
    assert tot_p == Decimal("87.00")

    return True

if __name__ == "__main__":
    try:
        if verificar():
            print("Casos executados: previsões e resultados conferem.")
        else:
            print("Verificações ainda incompletas.")
    except AssertionError as e:
        print(f"Falha na verificação: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")