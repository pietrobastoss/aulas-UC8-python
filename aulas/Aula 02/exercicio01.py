"""A02 — prática 1: campos em edição e registro confirmado."""

def registrar(campos, registro):
    # Normalize as pontas dos textos de nome e sobrenome
    nome = campos.get("nome", "").strip()
    sobrenome = campos.get("sobrenome", "").strip()
    idade_texto = campos.get("idade", "").strip()

    # Validação de campos obrigatórios (não vazios)
    if not nome or not sobrenome:
        return "Erro: Nome e sobrenome não podem estar vazios."

    # Validação e conversão da idade para inteiro maior que zero
    try:
        idade = int(idade_texto)
        if idade <= 0:
            return "Erro: A idade deve ser um número inteiro maior que zero."
    except ValueError:
        return "Erro: A idade deve ser um número inteiro válido."

    # Atualização do registro somente após a aprovação de todas as validações
    registro.clear()
    registro.update({
        "nome": nome,
        "sobrenome": sobrenome,
        "idade": idade
    })
    
    return f"Registro de {nome} {sobrenome} confirmado com sucesso!"


def exibir(registro):
    # Tratamento para ausência de registro
    if not registro:
        return "Nenhum cadastro registrado nesta sessão."
    
    return f"Último registro confirmado: {registro['nome']} {registro['sobrenome']}, {registro['idade']} anos."


def limpar(campos):
    # Esvazia os três textos editáveis mantendo o dicionário original
    campos["nome"] = ""
    campos["sobrenome"] = ""
    campos["idade"] = ""


if __name__ == "__main__":
    # Dicionários de estado
    campos = {"nome": "Lia", "sobrenome": "Costa", "idade": "18"}
    registro = {}

    print("--- Cenário 1: Consulta inicial antes de registrar ---")
    print(exibir(registro))

    print("\n--- Cenário 2: Registro válido ---")
    print(registrar(campos, registro))
    print(exibir(registro))

    print("\n--- Cenário 3: Limpar campos em edição ---")
    limpar(campos)
    print("Campos após limpar:", campos)
    print("Exibir após limpar campos (deve manter o registro intacto):")
    print(exibir(registro))

    print("\n--- Cenário 4: Tentativa inválida com registro anterior existente ---")
    campos.update({"nome": "Rui", "sobrenome": "Lima", "idade": "abc"})
    print(registrar(campos, registro))
    print("Exibir após falha (deve conservar o registro da Lia):")
    print(exibir(registro))

    print("\n--- Cenário 5: Novo registro válido substituindo o anterior ---")
    campos.update({"nome": "Rui", "sobrenome": "Lima", "idade": "22"})
    print(registrar(campos, registro))
    print(exibir(registro))