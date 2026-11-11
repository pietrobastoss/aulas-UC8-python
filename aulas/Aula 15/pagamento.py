# A15: assinaturas de apoio; traga sua implementação anterior.

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

FATORES = {'Dinheiro': '0.87', 'PIX': '0.87', 'Débito': '0.92', 'Crédito 1x': '1.00'}

def valor_monetario(texto, permitir_zero=True):
    """
    Valida e converte um texto monetário para um objeto Decimal arredondado a 2 casas.
    Aceita formatos como '10,50', 'R$ 10.50', '10.5', etc.
    """
    if texto is None:
        raise ValueError("Texto monetário não pode ser vazio.")
    
    # Remove símbolos de moeda e espaços em branco
    limpo = str(texto).strip()
    limpo = re.sub(r'^[a-zA-Z$R\s]+', '', limpo).strip()
    if not limpo:
        raise ValueError("Texto monetário vazio ou inválido.")

    # Normalização dos separadores decimais e de milhares
    if ',' in limpo and '.' in limpo:
        if limpo.rfind(',') > limpo.rfind('.'):
            # Formato brasileiro: 1.234,56
            limpo = limpo.replace('.', '').replace(',', '.')
        else:
            # Formato americano: 1,234.56
            limpo = limpo.replace(',', '')
    else:
        # Vírgula como delimitador decimal (ex: 12,50)
        limpo = limpo.replace(',', '.')

    try:
        valor = Decimal(limpo)
    except (InvalidOperation, ValueError):
        raise ValueError(f"Formato monetário inválido: '{texto}'.")

    if not permitir_zero and valor <= Decimal('0.00'):
        raise ValueError("O valor deve ser maior que zero.")
    if permitir_zero and valor < Decimal('0.00'):
        raise ValueError("O valor não pode ser negativo.")

    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


def preco_para_centavos(texto):
    """Converte um texto monetário diretamente para um inteiro representando centavos."""
    val_decimal = valor_monetario(texto, permitir_zero=True)
    return int((val_decimal * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def calcular_pagamento(subtotal_texto, forma):
    """
    Calcula o valor final após aplicar o fator da forma de pagamento escolhida.
    Retorna uma tupla (subtotal_decimal, fator_decimal, total_decimal).
    """
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento inválida: '{forma}'.")

    subtotal = valor_monetario(subtotal_texto, permitir_zero=False)
    fator = Decimal(FATORES[forma])
    
    total = (subtotal * fator).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return subtotal, fator, total
