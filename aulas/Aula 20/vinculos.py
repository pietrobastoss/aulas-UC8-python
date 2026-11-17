# A20: assinaturas de apoio; traga sua implementação anterior.
def validar_vinculos(alunos, planos, matriculas):
    """Verifica se o aluno e o plano referenciados na matrícula existem nas coleções."""
    # Garante suporte tanto para dicionários {id: nome} quanto para listas de dicionários [{"id": ...}]
    if isinstance(alunos, dict):
        alunos_ids = set(alunos.keys())
    else:
        alunos_ids = {a["id"] for a in alunos}
        
    if isinstance(planos, dict):
        planos_ids = set(planos.keys())
    else:
        planos_ids = {p["id"] for p in planos}
        
    # Verifica se os IDs da matrícula constam nas chaves válidas
    aluno_valido = matriculas.get("aluno_id") in alunos_ids
    plano_valido = matriculas.get("plano_id") in planos_ids
    
    return aluno_valido and plano_valido

def pode_excluir_aluno(codigo, matriculas):
    """Retorna False se o aluno possuir matrículas ativas vinculadas, impedindo exclusão órfã."""
    for m in matriculas:
        # Compatível tanto com dicionário de matrícula quanto com objeto/chave direta
        aluno_id = m.get("aluno_id") if isinstance(m, dict) else getattr(m, "aluno_id", None)
        if aluno_id == codigo:
            return False
    return True

if __name__ == "__main__":
    # Teste rápido local para conferir os resultados esperados do ensaio
    alunos_teste = {1: "Lia"}
    planos_teste = {7: "Mensal"}
    matricula_teste = {"aluno_id": 1, "plano_id": 7}
    
    print("Inicial:", validar_vinculos(alunos_teste, planos_teste, matricula_teste))
    
    # Mudar o nome conserva o ID e o vínculo
    alunos_teste[1] = "Lia Souza"
    print("Após nome:", validar_vinculos(alunos_teste, planos_teste, matricula_teste))
    
    # ID ausente deve retornar False
    matricula_teste["aluno_id"] = 99
    print("Após ID:", validar_vinculos(alunos_teste, planos_teste, matricula_teste))