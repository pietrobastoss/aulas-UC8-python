"""A01 — prática 2. Esqueleto funcional de janela com validação."""
import tkinter as tk
from tkinter import ttk

def conferir_cadastro():
    # Obtém os textos dos campos de entrada
    nome = entrada_nome.get()
    idade_texto = entrada_idade.get()

    # Validação do nome (retira as pontas e verifica se está vazio)
    nome_limpo = nome.strip()
    if not nome_limpo:
        resultado.configure(text="Erro: O nome não pode estar vazio ou conter apenas espaços.")
        return

    # Validação e conversão da idade para inteiro com tratamento de erro
    try:
        idade = int(idade_texto)
    except ValueError:
        resultado.configure(text="Erro: A idade deve ser um número inteiro válido (ex: 18).")
        return

    # Validação da regra de negócio (idade deve ser maior que zero)
    if idade <= 0:
        resultado.configure(text="Erro: A idade deve ser maior que zero.")
        return

    # Sucesso: exibe o cadastro conferido no rótulo
    resultado.configure(text=f"Cadastro conferido com sucesso!\nNome: {nome_limpo}\nIdade: {idade}")

# Configuração da interface gráfica principal
janela = tk.Tk()
janela.title("Conferir cadastro fictício")
janela.columnconfigure(1, weight=1)

# Rótulo e campo para o nome
ttk.Label(janela, text="Nome fictício:").grid(row=0, column=0, padx=12, pady=8, sticky="w")
entrada_nome = ttk.Entry(janela)
entrada_nome.grid(row=0, column=1, padx=12, pady=8, sticky="ew")

# Rótulo e campo para a idade
ttk.Label(janela, text="Idade fictícia:").grid(row=1, column=0, padx=12, pady=8, sticky="w")
entrada_idade = ttk.Entry(janela)
entrada_idade.grid(row=1, column=1, padx=12, pady=8, sticky="ew")

# Botão para disparar a conferência ligando ao callback
ttk.Button(janela, text="Conferir cadastro", command=conferir_cadastro).grid(row=2, column=0, columnspan=2, pady=8)

# Rótulo de feedback para o resultado
resultado = ttk.Label(janela, text="Nenhum cadastro conferido nesta sessão.", wraplength=360)
resultado.grid(row=3, column=0, columnspan=2, padx=12, pady=8, sticky="w")

# Foco inicial no campo de nome
entrada_nome.focus_set()
janela.mainloop()