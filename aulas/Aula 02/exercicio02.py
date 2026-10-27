"""A02 — prática 2: complete a lógica e os callbacks."""
import tkinter as tk
from tkinter import ttk


def registrar(campos, registro):
    # Ler e normalizar nome e sobrenome usando .strip()
    nome = campos.get("nome", "").strip()
    sobrenome = campos.get("sobrenome", "").strip()
    idade_texto = campos.get("idade", "").strip()

    # Validar se os campos de texto não estão vazios após o strip
    if not nome or not sobrenome:
        return "Erro: Nome e sobrenome não podem estar vazios."

    # Converter idade e validar se é inteiro maior que zero
    try:
        idade = int(idade_texto)
        if idade <= 0:
            return "Erro: A idade deve ser um número inteiro maior que zero."
    except ValueError:
        return "Erro: A idade deve ser um número inteiro válido."

    # Atualizar o registro somente após todas as validações passarem com sucesso
    registro.clear()
    registro.update({
        "nome": nome,
        "sobrenome": sobrenome,
        "idade": idade
    })
    
    return f"Registro de {nome} {sobrenome} confirmado com sucesso!"


def exibir(registro):
    # Tratar a ausência de registro e consultar o último válido
    if not registro:
        return "Nenhum cadastro registrado nesta sessão."
    
    return f"Último registro confirmado: {registro['nome']} {registro['sobrenome']}, {registro['idade']} anos."


def limpar(campos):
    # Esvaziar os três textos editáveis no dicionário
    campos["nome"] = ""
    campos["sobrenome"] = ""
    campos["idade"] = ""


def criar_janela():
    janela = tk.Tk()
    janela.title("Cadastro em memória — A02")
    janela.columnconfigure(1, weight=1)
    
    campos = {"nome": "", "sobrenome": "", "idade": ""}
    registro = {}

    ttk.Label(janela, text="Nome fictício:").grid(row=0, column=0, padx=12, pady=6, sticky="w")
    entrada_nome = ttk.Entry(janela)
    entrada_nome.grid(row=0, column=1, padx=12, pady=6, sticky="ew")
    
    ttk.Label(janela, text="Sobrenome fictício:").grid(row=1, column=0, padx=12, pady=6, sticky="w")
    entrada_sobrenome = ttk.Entry(janela)
    entrada_sobrenome.grid(row=1, column=1, padx=12, pady=6, sticky="ew")
    
    ttk.Label(janela, text="Idade fictícia:").grid(row=2, column=0, padx=12, pady=6, sticky="w")
    entrada_idade = ttk.Entry(janela)
    entrada_idade.grid(row=2, column=1, padx=12, pady=6, sticky="ew")

    def ao_registrar():
        # Copiar os textos atuais dos widgets Entry para o dicionário de campos
        campos["nome"] = entrada_nome.get()
        campos["sobrenome"] = entrada_sobrenome.get()
        campos["idade"] = entrada_idade.get()

        # Chamar a função de registro
        mensagem = registrar(campos, registro)
        
        # Atualizar os rótulos de aviso e o resultado da consulta
        aviso.configure(text=mensagem)
        resultado.configure(text=exibir(registro))

    def ao_exibir():
        # Consultar apenas o registro confirmado, ignorando o que está digitado nos campos
        resultado.configure(text=exibir(registro))
        aviso.configure(text="Consulta ao último registro confirmado realizada.")

    def ao_limpar():
        # Limpar os campos no dicionário e apagar o texto visual dos widgets Entry
        limpar(campos)
        entrada_nome.delete(0, tk.END)
        entrada_sobrenome.delete(0, tk.END)
        entrada_idade.delete(0, tk.END)
        
        # Devolver o foco para a entrada de nome
        entrada_nome.focus_set()
        
        aviso.configure(text="Campos em edição limpos. O registro confirmado permanece intacto.")

    ttk.Button(janela, text="Registrar", command=ao_registrar).grid(row=3, column=0, padx=12, pady=8)
    ttk.Button(janela, text="Exibir", command=ao_exibir).grid(row=3, column=1, padx=12, pady=8)
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(row=4, column=0, columnspan=2, pady=6)
    
    aviso = ttk.Label(janela, text="Preencha os dados fictícios e registre.", wraplength=390)
    aviso.grid(row=5, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    
    resultado = ttk.Label(janela, text="Nenhum cadastro registrado nesta sessão.", wraplength=390)
    resultado.grid(row=6, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    
    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()