from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

FATORES = {
    'Dinheiro': '0.87', 
    'PIX': '0.87', 
    'Débito': '0.92', 
    'Crédito 1x': '1.00'
}

def valor_monetario(texto, permitir_zero=True):
    """Valida e converte um texto de valor monetário para Decimal."""
    if texto is None:
        raise ValueError("Texto vazio ou inválido.")
    
    limpo = str(texto).strip()
    # Remove símbolos de moeda e espaços extras, mantendo números, pontos e vírgulas
    limpo = re.sub(r'[^\d.,]', '', limpo)
    
    if not limpo:
        raise ValueError("Texto vazio ou inválido.")

    # Substitui vírgula por ponto para conversão decimal padrão
    if ',' in limpo and '.' in limpo:
        # Se houver ambos, assume que o ponto é separador de milhar e a vírgula de decimal
        limpo = limpo.replace('.', '').replace(',', '.')
    elif ',' in limpo:
        limpo = limpo.replace(',', '.')

    try:
        valor = Decimal(limpo)
    except InvalidOperation as e:
        raise ValueError("Valor monetário inválido.") from e

    if valor < 0:
        raise ValueError("O valor não pode ser negativo.")
    
    if not permitir_zero and valor == 0:
        raise ValueError("O valor deve ser maior que zero.")

    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def preco_para_centavos(texto):
    """Converte um texto de preço em reais (ex: '10.50' ou 'R$ 10,50') para um inteiro em centavos."""
    valor = valor_monetario(texto, permitir_zero=True)
    return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))

def calcular_pagamento(subtotal_texto, forma):
    """Calcula o valor final do pagamento com base no subtotal e na forma escolhida."""
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento inválida: {forma}")

    subtotal_dec = valor_monetario(subtotal_texto, permitir_zero=True)
    fator = Decimal(FATORES[forma])
    
    total_calculado = (subtotal_dec * fator).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return total_calculado