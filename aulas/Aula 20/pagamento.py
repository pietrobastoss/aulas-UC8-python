# A17: assinaturas de apoio; traga sua implementação anterior.

from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

FATORES = {'Dinheiro': '0.87', 'PIX': '0.87', 'Débito': '0.92', 'Crédito 1x': '1.00'}

def valor_monetario(texto, permitir_zero=True):
    """Converte e valida um texto monetário para um objeto Decimal de alta precisão."""
    if texto is None:
        raise ValueError("O valor monetário não pode ser nulo.")
    
    limpo = str(texto).strip()
    if not limpo:
        raise ValueError("O campo de valor monetário está vazio.")
    
    # Remove símbolos de moeda e separadores de milhar indesejados
    limpo = re.sub(r'[R\$\s\.]', '', limpo)
    # Substitui a vírgula decimal por ponto
    limpo = limpo.replace(',', '.')
    
    try:
        valor = Decimal(limpo)
    except (InvalidOperation, ValueError) as e:
        raise ValueError("Formato de valor monetário inválido.") from e
        
    if valor < 0:
        raise ValueError("O valor monetário não pode ser negativo.")
    if not permitir_zero and valor == 0:
        raise ValueError("O valor monetário deve ser maior que zero.")
        
    return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calcular_pagamento(subtotal_texto, forma):
    """Calcula o subtotal, o desconto/acréscimo baseado na forma de pagamento e o total final arredondado."""
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento inválida: '{forma}'. Escolha entre: {list(FATORES.keys())}")
        
    subtotal = valor_monetario(subtotal_texto, permitir_zero=False)
    fator = Decimal(FATORES[forma])
    
    total = (subtotal * fator).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    diferenca = total - subtotal
    
    return {
        "subtotal": subtotal,
        "forma": forma,
        "fator": fator,
        "diferenca": diferenca,
        "total": total
    }

def preco_para_centavos(texto):
    """Converte um texto de preço em reais (ex: '5,50') para um valor inteiro em centavos (ex: 550)."""
    valor_dec = valor_monetario(texto, permitir_zero=False)
    centavos = (valor_dec * Decimal(100)).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return int(centavos)
