# A12: assinaturas de apoio; implementação completa do módulo de pagamento.
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re

FATORES = {'Dinheiro': '0.87', 'PIX': '0.87', 'Débito': '0.92', 'Crédito 1x': '1.00'}

def valor_monetario(texto, permitir_zero=True):
    """Valida e converte uma string de texto em um objeto Decimal monetário positivo."""
    if texto is None:
        raise ValueError("Texto vazio ou inválido.")
    
    # Remove espaços e formatações comuns de moeda (ex: 'R$', pontos de milhar)
    limpo = str(texto).strip()
    if limpo.upper().startswith('R$'):
        limpo = limpo[2:].strip()
    
    # Substitui ponto por vazio (milhar) e vírgula por ponto (decimal) se necessário
    if ',' in limpo and '.' in limpo:
        limpo = limpo.replace('.', '').replace(',', '.')
    elif ',' in limpo:
        limpo = limpo.replace(',', '.')

    try:
        valor = Decimal(limpo)
        if valor < 0:
            raise ValueError("O valor monetário não pode ser negativo.")
        if not permitir_zero and valor == 0:
            raise ValueError("O valor monetário deve ser maior que zero.")
        return valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError) as e:
        raise ValueError("Formato de valor monetário inválido.") from e


def preco_para_centavos(texto):
    """Converte um texto de preço ou valor monetário para um inteiro em centavos."""
    valor = valor_monetario(texto, permitir_zero=True)
    return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))


def calcular_pagamento(subtotal_texto, forma):
    """Calcula o valor final aplicando o fator de desconto/acréscimo correspondente à forma de pagamento."""
    if forma not in FATORES:
        raise ValueError(f"Forma de pagamento inválida: {forma}")
    
    subtotal = valor_monetario(subtotal_texto, permitir_zero=False)
    fator = Decimal(FATORES[forma])
    
    total_calculado = subtotal * fator
    total_centavos = int((total_calculado * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    
    # Retorna formatado ou em centavos/decimal dependendo do contrato anterior; 
    # mantendo compatibilidade com o retorno em Decimal quantizado:
    return (Decimal(total_centavos) / Decimal(100)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)