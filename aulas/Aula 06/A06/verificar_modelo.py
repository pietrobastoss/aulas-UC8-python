from aluno import Aluno


def verificar_independencia():
    lia = Aluno()
    rui = Aluno()

    # 1. Conferir que os objetos são instâncias distintas e possuem listas separadas
    assert lia is not rui, "Erro: 'lia' e 'rui' devem ser instâncias diferentes."
    assert lia.notas is not rui.notas, "Erro: As listas de notas não podem ser compartilhadas."
    assert lia.calcular_media() is None, "Erro: Média inicial de Lia deve ser None."
    assert rui.calcular_media() is None, "Erro: Média inicial de Rui deve ser None."

    # 2. Atualizar apenas Lia e verificar independência
    msg_lia = lia.atualizar("Lia Souza", "Turma 101", ["6", "7", "8", "9", "10"])
    assert "sucesso" in msg_lia.lower()
    
    # Previsão: Lia tem média 8.0 e notas preenchidas; Rui continua vazio
    assert lia.calcular_media() == 8.0, f"Média esperada de Lia: 8.0, obtida: {lia.calcular_media()}"
    assert rui.calcular_media() is None, "Erro: Rui não deveria possuir notas cadastradas."
    assert rui.nome == "", "Erro: O nome de Rui não pode ter sido alterado."
    assert rui.turma == "", "Erro: A turma de Rui não pode ter sido alterada."

    # 3. Atualizar Rui com outra lista (testando uso de vírgula decimal)
    msg_rui = rui.atualizar("Rui Lima", "Turma 102", ["5,0", "5", "5,5", "4,5", "5"])
    assert "sucesso" in msg_rui.lower()
    
    # Previsão: Média de Rui deve ser 5.0 e Lia permanece inalterada
    assert rui.calcular_media() == 5.0, f"Média esperada de Rui: 5.0, obtida: {rui.calcular_media()}"
    assert lia.calcular_media() == 8.0, "Erro: A média de Lia foi afetada pela atualização de Rui."
    assert len(lia.notas) == 5 and len(rui.notas) == 5

    return True


def verificar_validacao():
    aluno = Aluno()

    # 1. Configurar um estado válido inicial
    msg_valida = aluno.atualizar("Ana Silva", "Turma A", ["10", "0", "5", "8", "9"])
    assert "sucesso" in msg_valida.lower()
    assert aluno.nome == "Ana Silva"
    assert aluno.calcular_media() == 6.4

    # 2. Testar falha por quantidade incorreta de notas (preservando o estado anterior)
    msg_erro_qtd = aluno.atualizar("Ana Silva", "Turma A", ["10", "8", "9"])
    assert "Erro" in msg_erro_qtd
    # O registro válido anterior deve estar perfeitamente preservado
    assert aluno.nome == "Ana Silva"
    assert aluno.turma == "Turma A"
    assert aluno.calcular_media() == 6.4

    # 3. Testar falha na última nota (excedendo o limite de 10) após um estado válido
    msg_erro_limite = aluno.atualizar("Ana Silva", "Turma A", ["8", "8", "8", "8", "11"])
    assert "Erro" in msg_erro_limite
    # Garante que a tentativa inválida não sobrescreveu os dados anteriores
    assert aluno.calcular_media() == 6.4
    assert aluno.notas == [10.0, 0.0, 5.0, 8.0, 9.0]

    # 4. Testar valores nos limites exatos (0 e 10)
    msg_limites = aluno.atualizar("Teste Limites", "Turma B", ["0", "10", "0.0", "10.0", "5"])
    assert "sucesso" in msg_limites.lower()
    assert aluno.calcular_media() == 5.0

    return True


if __name__ == "__main__":
    independencia = verificar_independencia()
    validacao = verificar_validacao()
    if independencia and validacao:
        print("Verificações do modelo concluídas com sucesso!")
    else:
        print("Verificações incompletas; implemente e execute os casos.")