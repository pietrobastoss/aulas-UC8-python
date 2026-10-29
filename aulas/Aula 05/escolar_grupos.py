
"""A05 — complete: Escolar em grupos — A05."""
import tkinter as tk
from tkinter import ttk
from math import isfinite



def calcular(campos, registro):
    nome = campos.get("nome", "").strip()
    turma = campos.get("turma", "").strip()

    if not nome or not turma:
        return "Erro: Nome e turma não podem estar vazios."

    textos_notas = campos.get("notas", [])

    if len(textos_notas) != 5:
        return "Erro: São exigidas exatamente 5 notas."

    notas_numericas = []

    for texto in textos_notas:
        if not isinstance(texto, str) or texto.strip() == "":
            return "Erro: Todas as cinco notas devem ser preenchidas."

        try:
            numero = float(texto.strip().replace(",", "."))
        except ValueError:
            return f"Erro: '{texto}' não é um número válido."

        if not isfinite(numero):
            return "Erro: A nota precisa ser um número finito."

        if not 0 <= numero <= 10:
            return f"Erro: A nota {numero} está fora do intervalo de 0 a 10."

        notas_numericas.append(numero)

    media = sum(notas_numericas) / len(notas_numericas)

    # Atualiza somente depois de validar todos os dados.
    registro["nome"] = nome
    registro["turma"] = turma
    registro["notas"] = notas_numericas
    registro["media"] = media

    return "Sucesso: Registro escolar calculado e registrado."




def exibir(registro):
    if not registro or "media" not in registro:
        return "Nenhum registro escolar confirmado nesta sessão."

    nome = registro.get("nome", "")
    turma = registro.get("turma", "")
    notas = registro.get("notas", [])
    media = registro.get("media", 0)

    notas_str = ", ".join(f"{nota:.1f}" for nota in notas)

    return (
        f"Aluno(a): {nome} | Turma: {turma} | "
        f"Notas: [{notas_str}] | Média: {media:.1f}"
    )




def limpar(campos):
    campos["nome"] = ""
    campos["turma"] = ""
    campos["notas"] = ["", "", "", "", ""]



def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar em grupos — A05")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)

    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = {}

    ttk.Label(
        base,
        text="Sistema escolar fictício — organize os campos"
    ).grid(row=0, column=0, columnspan=2, pady=6, sticky="w")

    # Grupo de identificação
    identificacao = ttk.LabelFrame(
        base,
        text="Identificação",
        padding=10
    )
    identificacao.grid(row=1, column=0, sticky="ew", pady=5)

    # Grupo de notas
    grupo_notas = ttk.LabelFrame(
        base,
        text="Notas",
        padding=10
    )
    grupo_notas.grid(row=2, column=0, sticky="ew", pady=5)

    # Grupo de ações
    acoes = ttk.Frame(base)
    acoes.grid(row=3, column=0, sticky="ew", pady=5)

    # Configuração das colunas
    identificacao.columnconfigure(1, weight=1)
    grupo_notas.columnconfigure(1, weight=1)
    acoes.columnconfigure(0, weight=1)
    acoes.columnconfigure(1, weight=1)

    # Campos de identificação
    ttk.Label(
        identificacao,
        text="Nome fictício:"
    ).grid(row=0, column=0, padx=6, pady=4, sticky="w")

    entrada_nome = ttk.Entry(identificacao)
    entrada_nome.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

    ttk.Label(
        identificacao,
        text="Turma fictícia:"
    ).grid(row=1, column=0, padx=6, pady=4, sticky="w")

    entrada_turma = ttk.Entry(identificacao)
    entrada_turma.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

    # Campos das cinco notas
    entradas_notas = []

    for numero in range(1, 6):
        ttk.Label(
            grupo_notas,
            text=f"Nota {numero} (0 a 10):"
        ).grid(row=numero-1, column=0, padx=6, pady=4, sticky="w")

        entrada = ttk.Entry(grupo_notas)
        entrada.grid(row=numero-1, column=1, padx=6, pady=4, sticky="ew")

        entradas_notas.append(entrada)

    # Callback do botão Calcular

    def ao_calcular():  
        campos["nome"] = entrada_nome.get()
        campos["turma"] = entrada_turma.get()
        campos["notas"] = [entrada.get() for entrada in entradas_notas]

        msg = calcular(campos, registro)
        aviso.configure(text=msg)
        resultado.configure(text=exibir(registro))


    # Callback do botão Exibir
    
    def ao_exibir():
        resultado.configure(text=exibir(registro))
        aviso.configure(text="Exibindo o último registro confirmado.")




    # Callback do botão Limpar
    def ao_limpar():
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)

        for entrada in entradas_notas:
            entrada.delete(0, tk.END)

        limpar(campos)
        entrada_nome.focus_set()

        aviso.configure(text="Campos de edição limpos. Registro anterior mantido.")
        resultado.configure(text=exibir(registro))


    # Botões
    ttk.Button(
        acoes,
        text="Calcular média",
        command=ao_calcular
    ).grid(row=0, column=0, padx=4, pady=6)

    ttk.Button(
        acoes,
        text="Exibir",
        command=ao_exibir
    ).grid(row=0, column=1, padx=4, pady=6)

    ttk.Button(
        acoes,
        text="Limpar campos",
        command=ao_limpar
    ).grid(row=1, column=0, columnspan=2, padx=4, pady=6)

    # Aviso
    aviso = ttk.Label(
        base,
        text="Use dados fictícios e confira as cinco notas.",
        wraplength=430
    )
    aviso.grid(row=4, column=0, columnspan=2, pady=6, sticky="w")

    # Resultado
    resultado = ttk.Label(
        base,
        text="Nenhum registro escolar confirmado nesta sessão.",
        wraplength=430
    )
    resultado.grid(row=5, column=0, columnspan=2, pady=6, sticky="w")

    entrada_nome.focus_set()

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
