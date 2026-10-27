"""A03 — complete as funções antes de conectá-las à janela."""


def ler_decimal(texto):
    """Trata vírgula como ponto e converte a string para float."""
    texto_limpo = texto.strip().replace(",", ".")
    return float(texto_limpo)


def calcular(campos, registro):
    # 1. Tentar ler os três campos e tratar erro de conversão
    try:
        reais = ler_decimal(campos.get("reais", ""))
        cotacao_dolar = ler_decimal(campos.get("cotacao_dolar", ""))
        cotacao_euro = ler_decimal(campos.get("cotacao_euro", ""))
    except ValueError:
        return "Erro: Todos os campos devem conter valores numéricos válidos."

    # 2. Validar regras de negócio
    if reais < 0:
        return "Erro: O valor em reais não pode ser negativo."

    if cotacao_dolar <= 0 or cotacao_euro <= 0:
        return "Erro: As cotações do dólar e do euro devem ser estritamente maiores que zero."

    # 3. Realizar as conversões
    dolares = reais / cotacao_dolar
    euros = reais / cotacao_euro

    # 4. Atualizar o registro SOMENTE após todas as validações e cálculos
    registro.update(
        {
            "reais": reais,
            "cotacao_dolar": cotacao_dolar,
            "cotacao_euro": cotacao_euro,
            "dolares": dolares,
            "euros": euros,
        }
    )

    return "Conversão realizada e registrada com sucesso."


def exibir(registro):
    # Tratar ausência de conversão confirmada
    if not registro:
        return "Nenhuma conversão confirmada nesta sessão."

    # Consultar apenas o registro confirmado
    return (
        f"Última conversão confirmada:\n"
        f"  - Valor: R$ {registro['reais']:.2f}\n"
        f"  - Cotação USD: R$ {registro['cotacao_dolar']} | Resultado: $ {registro['dolares']:.2f}\n"
        f"  - Cotação EUR: R$ {registro['cotacao_euro']} | Resultado: € {registro['euros']:.2f}"
    )


def limpar(campos):
    # Esvaziar os três campos, sem alterar o registro existente
    campos["reais"] = ""
    campos["cotacao_dolar"] = ""
    campos["cotacao_euro"] = ""


if __name__ == "__main__":
    campos = {"reais": "100", "cotacao_dolar": "5", "cotacao_euro": "4"}
    registro = {}

    print("=== 1. Consulta inicial (registro vazio) ===")
    print(exibir(registro))
    print()

    print("=== 2. Cálculo válido (100 / 5 / 4) ===")
    print(calcular(campos, registro))
    print(exibir(registro))
    print()

    print("=== 3. Edição dos campos sem confirmar (simulando digitação) ===")
    campos["reais"] = "200"
    campos["cotacao_dolar"] = "10"
    # Exibir deve continuar mostrando os dados do registro anterior (100 / 5 / 4)
    print(exibir(registro))
    print()

    print("=== 4. Tentativa inválida (cotação com texto) ===")
    campos["cotacao_euro"] = "abc"
    print(calcular(campos, registro))
    # O registro não deve ter sido alterado pelo erro
    print(exibir(registro))
    print()

    print("=== 5. Tentativa com reais negativos ===")
    campos["reais"] = "-50"
    campos["cotacao_dolar"] = "5"
    campos["cotacao_euro"] = "4"
    print(calcular(campos, registro))
    print(exibir(registro))
    print()

    print("=== 6. Tentativa com cotação zero ou negativa ===")
    campos["reais"] = "100"
    campos["cotacao_dolar"] = "0"
    print(calcular(campos, registro))
    print(exibir(registro))
    print()

    print("=== 7. Correção válida com vírgula (100,50 / 5 / 4) ===")
    campos["reais"] = "100,50"
    campos["cotacao_dolar"] = "5"
    campos["cotacao_euro"] = "4"
    print(calcular(campos, registro))
    print(exibir(registro))
    print()

    print("=== 8. Teste com reais zero (0 / 5 / 4) ===")
    campos["reais"] = "0"
    print(calcular(campos, registro))
    print(exibir(registro))
    print()

    print("=== 9. Limpar campos ===")
    limpar(campos)
    print(f"Campos após limpar: {campos}")
    print(exibir(registro))  # Registro permanece intacto