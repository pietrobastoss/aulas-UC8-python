from math import isfinite


class Aluno:
    def __init__(self):
        # Cria atributos iniciais vazios e uma lista de notas exclusiva para cada instância
        self.nome = ""
        self.turma = ""
        self.notas = []

    def atualizar(self, nome, turma, notas_texto):
        # 1. Validação de Nome e Turma
        if not isinstance(nome, str) or not nome.strip():
            return "Erro: O nome não pode estar vazio."
        if not isinstance(turma, str) or not turma.strip():
            return "Erro: A turma não pode estar vazia."

        # 2. Validação da quantidade de notas
        if not isinstance(notas_texto, (list, tuple)) or len(notas_texto) != 5:
            return "Erro: É necessário fornecer exatamente cinco notas."

        # 3. Processamento e validação individual de cada nota
        notas_validadas = []
        for i, item in enumerate(notas_texto, start=1):
            if isinstance(item, (int, float)):
                texto_limpo = str(item).strip()
            elif isinstance(item, str):
                texto_limpo = item.strip()
            else:
                return f"Erro: A nota {i} possui formato inválido."

            if not texto_limpo:
                return f"Erro: A nota {i} não pode ser vazia."

            # Aceitar tanto ponto quanto vírgula como separador decimal
            texto_formatado = texto_limpo.replace(",", ".")

            try:
                valor = float(texto_formatado)
            except ValueError:
                return f"Erro: A nota {i} ('{item}') não é um número válido."

            # Validações de finitude e limites (0 a 10 inclusive)
            if not isfinite(valor):
                return f"Erro: A nota {i} deve ser um número finito."
            if valor < 0.0 or valor > 10.0:
                return f"Erro: A nota {i} deve estar entre 0 e 10."

            notas_validadas.append(valor)

        # 4. Confirmação integral (só atualiza os atributos se TUDO estiver válido)
        self.nome = nome.strip()
        self.turma = turma.strip()
        self.notas = notas_validadas

        return "Atualização realizada com sucesso!"

    def calcular_media(self):
        # Retorna None se ainda não houver notas confirmadas
        if not self.notas:
            return None
        # Calcula a média sem arredondar no modelo
        return sum(self.notas) / len(self.notas)

    def resumo(self):
        # Exibe apenas os atributos confirmados e formata a média com uma casa decimal
        media = self.calcular_media()
        if media is None:
            return "Nenhum registro escolar confirmado."
        
        return f"Nome: {self.nome} | Turma: {self.turma} | Média: {media:.1f}"