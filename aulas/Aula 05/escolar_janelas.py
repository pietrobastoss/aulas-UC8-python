
"""A05 — Escolar com consulta — A05."""

import tkinter as tk
from tkinter import ttk
from math import isfinite
from pathlib import Path


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


def inserir_marca(container, caminho=None):
    if caminho is None:
        caminho = Path(__file__).resolve().parent / "marca-a05.png"
    else:
        caminho = Path(caminho)

    try:
        imagem = tk.PhotoImage(file=str(caminho))
        rotulo = ttk.Label(container, image=imagem)
        rotulo.image = imagem
        return rotulo

    except (tk.TclError, OSError):
        return ttk.Label(
            container,
            text="Sistema escolar fictício — A05"
        )


def abrir_consulta(principal, registro):
    if not registro or "media" not in registro:
        return None

    texto = exibir(registro)

    consulta = tk.Toplevel(principal)
    consulta.title("Consulta escolar")
    consulta.geometry("450x180")
    consulta.transient(principal)

    quadro = ttk.Frame(consulta, padding=15)
    quadro.pack(fill="both", expand=True)

    ttk.Label(
        quadro,
        text="Último registro confirmado",
        font=("Arial", 12, "bold")
    ).pack(pady=8)

    ttk.Label(
        quadro,
        text=texto,
        wraplength=400,
        justify="left"
    ).pack(pady=8)

    def fechar():
        consulta.destroy()

    ttk.Button(
        quadro,
        text="Fechar",
        command=fechar
    ).pack(pady=8)

    consulta.bind("<Escape>", lambda evento: fechar())
    consulta.protocol("WM_DELETE_WINDOW", fechar)
    consulta.focus_set()

    return consulta


def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar com consulta — A05")
    janela.geometry("520x650")

    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)

    campos = {
        "nome": "",
        "turma": "",
        "notas": ["", "", "", "", ""]
    }

    registro = {}

    inserir_marca(base).grid(
        row=0, column=0, pady=6, sticky="w"
    )

    # Grupo de identificação
    identificacao = ttk.LabelFrame(
        base, text="Identificação", padding=8
    )
    identificacao.grid(row=1, column=0, sticky="ew", pady=6)
    identificacao.columnconfigure(1, weight=1)

    # Grupo de notas
    grupo_notas = ttk.LabelFrame(
        base, text="Notas", padding=8
    )
    grupo_notas.grid(row=2, column=0, sticky="ew", pady=6)
    grupo_notas.columnconfigure(1, weight=1)

    # Grupo de ações
    acoes = ttk.Frame(base)
    acoes.grid(row=3, column=0, sticky="ew", pady=6)

    # Campos de identificação
    ttk.Label(
        identificacao, text="Nome fictício:"
    ).grid(row=0, column=0, padx=6, pady=4, sticky="w")

    entrada_nome = ttk.Entry(identificacao)
    entrada_nome.grid(
        row=0, column=1, padx=6, pady=4, sticky="ew"
    )

    ttk.Label(
        identificacao, text="Turma fictícia:"
    ).grid(row=1, column=0, padx=6, pady=4, sticky="w")

    entrada_turma = ttk.Entry(identificacao)
    entrada_turma.grid(
        row=1, column=1, padx=6, pady=4, sticky="ew"
    )

    # Campos das cinco notas
    entradas_notas = []

    for numero in range(1, 6):
        ttk.Label(
            grupo_notas,
            text=f"Nota {numero} (0 a 10):"
        ).grid(
            row=numero - 1,
            column=0,
            padx=6,
            pady=4,
            sticky="w"
        )

        entrada = ttk.Entry(grupo_notas)
        entrada.grid(
            row=numero - 1,
            column=1,
            padx=6,
            pady=4,
            sticky="ew"
        )

        entradas_notas.append(entrada)

    # Botão calcular
    def ao_calcular():
        campos["nome"] = entrada_nome.get()
        campos["turma"] = entrada_turma.get()
        campos["notas"] = [
            entrada.get() for entrada in entradas_notas
        ]

        mensagem = calcular(campos, registro)
        aviso.configure(text=mensagem)

        if mensagem.startswith("Sucesso"):
            resultado.configure(text=exibir(registro))

    # Botão consultar
    def ao_exibir():
        mensagem = exibir(registro)
        resultado.configure(text=mensagem)

        if "media" not in registro:
            aviso.configure(text=mensagem)
            return

        aviso.configure(text="Consulta aberta.")
        abrir_consulta(janela, registro)

    # Botão limpar
    def ao_limpar():
        limpar(campos)

        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)

        for entrada in entradas_notas:
            entrada.delete(0, tk.END)

        aviso.configure(
            text="Campos limpos. O último registro continua salvo."
        )

        entrada_nome.focus_set()

    # Botões
    ttk.Button(
        acoes,
        text="Calcular média",
        command=ao_calcular
    ).grid(row=0, column=0, padx=4, pady=6)

    ttk.Button(
        acoes,
        text="Consultar",
        command=ao_exibir
    ).grid(row=0, column=1, padx=4, pady=6)

    ttk.Button(
        acoes,
        text="Limpar campos",
        command=ao_limpar
    ).grid(row=0, column=2, padx=4, pady=6)

    # Mensagens
    aviso = ttk.Label(
        base,
        text="Use dados fictícios e confira as cinco notas.",
        wraplength=470
    )
    aviso.grid(row=4, column=0, pady=6, sticky="w")

    resultado = ttk.Label(
        base,
        text="Nenhum registro escolar confirmado nesta sessão.",
        wraplength=470
    )
    resultado.grid(row=5, column=0, pady=6, sticky="w")

    entrada_nome.focus_set()

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
