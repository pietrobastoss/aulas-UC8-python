# A14: integre sua versão anterior; preserve-a em outra pasta.

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from modelos import Pedido
from repositorio import RepositorioSqlite
from perfis import SessaoDemo


def criar_janela():
    janela = tk.Tk()
    janela.title("A14 — Pizzaria & Sorveteria (Produtos em SQLite)")
    janela.geometry("640x540")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    # Definção do banco de dados SQLite fictício local
    caminho_db = Path("dados_pizzaria.db").resolve()
    repo = RepositorioSqlite(caminho_db)

    # Estado da sessão e do pedido (mantidos em memória nesta etapa)
    sessao = SessaoDemo()
    pedido = Pedido()

    # Container Principal
    base = ttk.Frame(janela, padding=10)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(1, weight=1)

    # Rótulo superior informativo sobre o banco
    lbl_banco = ttk.Label(
        base, 
        text=f"Banco SQLite: {caminho_db.name}", 
        font=("Arial", 9, "italic"),
        foreground="gray"
    )
    lbl_banco.grid(row=0, column=0, sticky="w", pady=(0, 6))

    # Notebook (Abas)
    notebook = ttk.Notebook(base)
    notebook.grid(row=1, column=0, sticky="nsew")

    # ----------------------------------------------------
    # ABA 1: PRODUTOS (PERSISTÊNCIA EM SQLITE)
    # ----------------------------------------------------
    aba_produtos = ttk.Frame(notebook, padding=12)
    aba_produtos.columnconfigure(1, weight=1)
    aba_produtos.rowconfigure(3, weight=1)
    notebook.add(aba_produtos, text=" Cadastro de Produtos ")

    # Formulário de Entrada
    ttk.Label(aba_produtos, text="Nome do Produto:").grid(row=0, column=0, sticky="w", pady=4)
    entry_nome = ttk.Entry(aba_produtos)
    entry_nome.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=4)
    entry_nome.insert(0, "Picolé d'água")

    ttk.Label(aba_produtos, text="Preço Unitário (R$):").grid(row=1, column=0, sticky="w", pady=4)
    entry_preco = ttk.Entry(aba_produtos)
    entry_preco.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=4)
    entry_preco.insert(0, "4,50")

    aviso_produtos = ttk.Label(aba_produtos, text="Preencha os dados e clique em Salvar.", foreground="gray")
    aviso_produtos.grid(row=2, column=0, columnspan=2, sticky="w", pady=6)

    # Tabela de Listagem de Produtos (Treeview)
    colunas = ("id", "nome", "preco_centavos")
    tabela_produtos = ttk.Treeview(aba_produtos, columns=colunas, show="headings", height=8)
    tabela_produtos.heading("id", text="ID")
    tabela_produtos.heading("nome", text="Nome do Produto")
    tabela_produtos.heading("preco_centavos", text="Preço (Centavos)")

    tabela_produtos.column("id", width=60, anchor="center")
    tabela_produtos.column("nome", width=280, anchor="w")
    tabela_produtos.column("preco_centavos", width=120, anchor="e")
    tabela_produtos.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=6)

    # Scrollbar para a Tabela
    scroll = ttk.Scrollbar(aba_produtos, orient="vertical", command=tabela_produtos.yview)
    tabela_produtos.configure(yscrollcommand=scroll.set)
    scroll.grid(row=3, column=2, sticky="ns", pady=6)

    def atualizar_listagem():
        """Consulta o banco SQLite e redesenha os itens na Treeview."""
        for item in tabela_produtos.get_children():
            tabela_produtos.delete(item)
        
        produtos = repo.listar_produtos()
        for prod in produtos:
            tabela_produtos.insert("", "end", iid=prod["id"], values=(prod["id"], prod["nome"], prod["preco_centavos"]))

    def salvar_produto():
        """Callback do botão Salvar: lê entradas, grava no SQLite e atualiza a lista após sucesso."""
        nome = entry_nome.get()
        preco_txt = entry_preco.get()

        try:
            # Tenta inserir no banco (valida nome e converte preço defensivamente)
            novo_id = repo.adicionar_produto(nome, preco_txt)
            
            # Anúncio de SUCESSO e limpeza somente APÓS a gravação bem-sucedida
            atualizar_listagem()
            aviso_produtos.configure(text=f"Sucesso! Produto ID {novo_id} gravado no SQLite.", foreground="green")
            messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso (ID: {novo_id}).")
            
            entry_nome.delete(0, tk.END)
            entry_preco.delete(0, tk.END)
            entry_nome.focus_set()

        except Exception as e:
            # Em caso de FALHA, preserva os dados digitados e avisa o usuário
            aviso_produtos.configure(text=f"Erro: {e}", foreground="red")
            messagebox.showerror("Falha ao Salvar", f"Não foi possível salvar o produto:\n{e}\n\nSeus dados editados foram mantidos para correção.")

    btn_salvar = ttk.Button(aba_produtos, text="Salvar no Banco (SQLite)", command=salvar_produto)
    btn_salvar.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(4, 0))

    # Carrega os produtos existentes no banco ao iniciar a janela
    atualizar_listagem()

    # ----------------------------------------------------
    # ABA 2: PEDIDO E SESSÃO (MANTIDOS DAS AULAS ANTERIORES)
    # ----------------------------------------------------
    aba_pedido = ttk.Frame(notebook, padding=12)
    notebook.add(aba_pedido, text=" Pedidos em Memória ")

    ttk.Label(
        aba_pedido, 
        text="A montagem de pedidos e comprovantes CSV continua ativa em memória nesta etapa.",
        wraplength=480
    ).pack(anchor="w", pady=10)

    # Rodapé informativo para navegação por teclado
    ttk.Label(
        base, 
        text="Pressione Tab/Shift+Tab para percorrer os campos. Enter ou Barra de Espaço aciona o botão em foco.", 
        font=("Arial", 8), 
        foreground="gray"
    ).grid(row=2, column=0, sticky="w", pady=(8, 0))

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()