"""A04 — complete as funções e teste as cinco notas no terminal."""

def calcular(campos, registro):
    # 1. Normalizar nome e turma (removendo espaços nas pontas) e recusar texto vazio
    nome = campos.get("nome", "").strip()
    turma = campos.get("turma", "").strip()
    
    if not nome or not turma:
        return "Erro: Nome e turma não podem estar vazios."
    
    textos_notas = campos.get("notas", [])
    
    # 2. Conferir a presença de exatamente cinco notas
    if len(textos_notas) != 5:
        return f"Erro: São exigidas exatamente 5 notas (foram encontradas {len(textos_notas)})."
    
    # 3. Converter cada texto, validar se está entre 0 e 10 e criar uma nova lista numérica
    notas_numericas = []
    for texto in textos_notas:
        if not isinstance(texto, str) or texto.strip() == "":
            return "Erro: Todas as cinco notas devem ser preenchidas."
        
        try:
            # Substitui vírgula por ponto para aceitar formato decimal brasileiro
            numero = float(texto.strip().replace(",", "."))
        except ValueError:
            return f"Erro: '{texto}' não é um número válido."
        
        if not (0.0 <= numero <= 10.0):
            return f"Erro: A nota {numero} está fora do intervalo permitido (0 a 10)."
        
        notas_numericas.append(numero)
    
    # 4. Calcular a média simples com sum e len
    media = sum(notas_numericas) / len(notas_numericas)
    
    # 5. Confirmar nome, turma, notas e média somente após validar tudo
    registro["nome"] = nome
    registro["turma"] = turma
    registro["notas"] = notas_numericas
    registro["media"] = media
    
    return "Sucesso: Registro escolar calculado e confirmado."


def exibir(registro):
    # Tratar ausência de registro confirmado
    if not registro or "media" not in registro:
        return "Nenhum registro escolar confirmado nesta sessão."
    
    nome = registro.get("nome")
    turma = registro.get("turma")
    notas = registro.get("notas", [])
    media = registro.get("media")
    
    # Formatar as notas e a média com uma casa decimal
    notas_str = ", ".join(f"{nota:.1f}" for nota in notas)
    return f"Aluno(a): {nome} | Turma: {turma} | Notas: [{notas_str}] | Média: {media:.1f}"


def limpar(campos):
    # Esvaziar nome, turma e os cinco textos de notas (o registro confirmado não é alterado)
    campos["nome"] = ""
    campos["turma"] = ""
    campos["notas"] = ["", "", "", "", ""]


if __name__ == "__main__":
    campos = {"nome": "Lia", "turma": "T1", "notas": ["6", "7", "8", "9", "10"]}
    registro = {}
    
    print("--- 1. Exibir antes do primeiro cálculo ---")
    print(exibir(registro))
    
    print("\n--- 2. Calcular com dados válidos ---")
    print(calcular(campos, registro))
    print(exibir(registro))
    
    print("\n--- 3. Simular erro na última nota (tentativa inválida) ---")
    campos_com_erro = {"nome": "Rui", "turma": "T2", "notas": ["5", "5", "5", "5", "abc"]}
    print(calcular(campos_com_erro, registro))
    
    print("\n--- 4. Verificar se o registro anterior foi preservado ---")
    print(exibir(registro))  
    
    print("\n--- 5. Testar lista com quantidade incorreta (ex: 4 notas) ---")
    campos_quatro = {"nome": "Ana", "turma": "T1", "notas": ["7", "8", "9", "10"]}
    print(calcular(campos_quatro, registro))
    print(exibir(registro))