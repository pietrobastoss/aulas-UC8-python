"""A04 — complete a lógica e os callbacks do sistema escolar."""
import tkinter as tk
from tkinter import ttk


def calcular(campos, registro):
    nome = campos.get("nome", "").strip()
    turma = campos.get("turma", "").strip()

    if not nome or not turma:
        return "Erro: Nome e turma não podem estar vazios."
    textos_notas = campos.get("notas", [])

    # Conferir presença de exatamente 5 notas
    if len(textos_notas) != 5:
        return f"Erro: São exigidas exatamente 5 notas (Foram encontradas {len(textos_notas)})."
    
    notas_numericas = []
    for texto in textos_notas: 
        if not isinstance(texto, str) or texto.strip() == "":
            return "Erro: Todas as cinco notas devem ser preenchidas."
        
        try:
            numero = float(texto.strip().replace(",", "."))
        except ValueError:
            return f"Erro: '{texto}' não é um número válido"
        if not (0.0 <= numero <= 10.0):
            return f"Erro: A nota {numero} está fora do intervalo permitido"
        
        notas_numericas.append(numero)

    media = sum(notas_numericas) / len(notas_numericas)

    registro["nome"] = nome
    registro["turma"] = turma
    registro["notas"] = notas_numericas
    registro["media"] = media

    return "Sucesso: Registro escolar calculado e registrado"


def exibir(registro):
    # Consulta apenas o último registro confirmado
    if not registro or "media" not in registro:
        return "Nenhum registro escolar confirmado nesta sessão"

    nome = registro.get("nome")
    turma = registro.get("turma")
    notas = registro.get("notas", [])
    media = registro.get("media")

    notas_str = ", ".join(f"{nota:.1f}" for nota in notas)
    return f"Aluno(a): {nome} | Turma: {turma} | Notas: [{notas_str}] | Média: {media:.1f}"


def limpar(campos):
    campos["nome"] = ""
    campos["turma"] = ""
    # CORRIGIDO: Agora limpa exatamente 5 campos de notas vazios
    campos["notas"] = ["", "", "", "", ""]


def criar_janela():
    janela = tk.Tk()
    janela.title("Sistema escolar fictício — A04")
    janela.columnconfigure(1, weight=1)
    campos = {"nome": "", "turma": "", "notas": ["", "", "", "", ""]}
    registro = {}

    ttk.Label(janela, text="Dados fictícios. Cinco notas de 0 a 10; média simples.", wraplength=440).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    ttk.Label(janela, text="Nome fictício:").grid(row=1, column=0, padx=12, pady=4, sticky="w")
    entrada_nome = ttk.Entry(janela)
    entrada_nome.grid(row=1, column=1, padx=12, pady=4, sticky="ew")
    ttk.Label(janela, text="Turma fictícia:").grid(row=2, column=0, padx=12, pady=4, sticky="w")
    entrada_turma = ttk.Entry(janela)
    entrada_turma.grid(row=2, column=1, padx=12, pady=4, sticky="ew")
    entradas_notas = []

    for numero in range(1, 6):
        ttk.Label(janela, text=f"Nota {numero} (0 a 10):").grid(row=numero+2, column=0, padx=12, pady=4, sticky="w")
        entrada = ttk.Entry(janela)
        entrada.grid(row=numero+2, column=1, padx=12, pady=4, sticky="ew")
        entradas_notas.append(entrada)

    def ao_calcular():
       textos_lidos = [e.get() for e in entradas_notas]
       campos["nome"] = entrada_nome.get()
       campos["turma"] = entrada_turma.get()
       campos["notas"] = textos_lidos

       msg = calcular(campos, registro)
       aviso.configure(text=msg)
       resultado.configure(text=exibir(registro))

    def ao_exibir():
       resultado.configure(text=exibir(registro))
       aviso.configure(text="Exibindo o último registro confirmado.")

    def ao_limpar():
       entrada_nome.delete(0, tk.END)
       entrada_turma.delete(0, tk.END)
       for entrada in entradas_notas:
           inter = entrada.delete(0, tk.END) # limpa os widgets Entry individualmente

       limpar(campos)
       entrada_nome.focus_set()

       aviso.configure(text="Campos de edição limpos. Registro anterior mantido.")
       resultado.configure(text=exibir(registro))

    ttk.Button(janela, text="Calcular média", command=ao_calcular).grid(row=8, column=0, padx=12, pady=6)
    ttk.Button(janela, text="Exibir", command=ao_exibir).grid(row=8, column=1, padx=12, pady=6)
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(row=9, column=0, columnspan=2, pady=4)
    
    aviso = ttk.Label(janela, text="Preencha nome, turma e as cinco notas fictícias.", wraplength=440)
    aviso.grid(row=10, column=0, columnspan=2, padx=12, pady=6, sticky="w")
    
    resultado = ttk.Label(janela, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=440)
    resultado.grid(row=11, column=0, columnspan=2, padx=12, pady=6, sticky="w")
    
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()