# A15: integre sua versão anterior; preserve-a em outra pasta.
"""
Módulo de interface gráfica principal (UC8 - Aula 15).
Integra o CRUD completo de produtos, início da gestão de clientes
e persistência em SQLite via RepositorioSqlite.
"""

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from repositorio import RepositorioSqlite
from perfis import SessaoDemo


def criar_janela():
    janela = tk.Tk()
    janela.title("A15 — Pizzaria & Sorveteria (CRUD Completo)")
    janela.geometry("680x580")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    # Banco de dados SQLite local
    caminho_db = Path("dados_pizzaria.db").resolve()
    repo = RepositorioSqlite(caminho_db)
    sessao = SessaoDemo()

    # Variável de controle para o ID selecionado no CRUD de Produtos (None = modo Inclusão)
    id_produto_selecionado = tk.IntVar(value=0)

    # Container Principal
    base = ttk.Frame(janela, padding=10)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(1, weight=1)

    # Rótulo superior informativo
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
    # ABA 1: PRODUTOS (CRUD COMPLETO)
    # ----------------------------------------------------
    aba_produtos = ttk.Frame(notebook, padding=12)
    aba_produtos.columnconfigure(1, weight=1)
    aba_produtos.rowconfigure(4, weight=1)
    notebook.add(aba_produtos, text=" CRUD de Produtos ")

    # Formulário de Entrada
    ttk.Label(aba_produtos, text="Nome do Produto:").grid(row=0, column=0, sticky="w", pady=4)
    entry_nome_prod = ttk.Entry(aba_produtos)
    entry_nome_prod.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=4)

    ttk.Label(aba_produtos, text="Preço Unitário (R$):").grid(row=1, column=0, sticky="w", pady=4)
    entry_preco_prod = ttk.Entry(aba_produtos)
    entry_preco_prod.grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=4)

    lbl_modo_prod = ttk.Label(aba_produtos, text="Modo: Inclusão de Novo Produto", foreground="blue", font=("Arial", 9, "bold"))
    lbl_modo_prod.grid(row=2, column=0, columnspan=2, sticky="w", pady=4)

    aviso_produtos = ttk.Label(aba_produtos, text="Selecione um item na tabela para editar/excluir ou preencha para incluir.", foreground="gray")
    aviso_produtos.grid(row=3, column=0, columnspan=2, sticky="w", pady=4)

    # Tabela (Treeview) de Produtos
    colunas_prod = ("id", "nome", "preco_centavos")
    tabela_produtos = ttk.Treeview(aba_produtos, columns=colunas_prod, show="headings", height=7)
    tabela_produtos.heading("id", text="ID")
    tabela_produtos.heading("nome", text="Nome do Produto")
    tabela_produtos.heading("preco_centavos", text="Preço (Centavos)")

    tabela_produtos.column("id", width=60, anchor="center")
    tabela_produtos.column("nome", width=280, anchor="w")
    tabela_produtos.column("preco_centavos", width=120, anchor="e")
    tabela_produtos.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=6)

    scroll_prod = ttk.Scrollbar(aba_produtos, orient="vertical", command=tabela_produtos.yview)
    tabela_produtos.configure(yscrollcommand=scroll_prod.set)
    scroll_prod.grid(row=4, column=2, sticky="ns", pady=6)

    def atualizar_listagem_produtos():
        """Atualiza a Treeview de produtos consultando o SQLite."""
        for item in tabela_produtos.get_children():
            tabela_produtos.delete(item)
        for prod in repo.listar_produtos():
            tabela_produtos.insert("", "end", iid=prod["id"], values=(prod["id"], prod["nome"], prod["preco_centavos"]))

    def limpar_formulario_produtos():
        """Reseta o formulário para o modo de Inclusão."""
        id_produto_selecionado.set(0)
        entry_nome_prod.delete(0, tk.END)
        entry_preco_prod.delete(0, tk.END)
        lbl_modo_prod.configure(text="Modo: Inclusão de Novo Produto", foreground="blue")
        aviso_produtos.configure(text="Preencha os dados e clique em Salvar.", foreground="gray")
        entry_nome_prod.focus_set()

    def ao_selecionar_produto(event):
        """Carrega os dados do item selecionado na Treeview para o formulário (Modo Edição)."""
        selecao = tabela_produtos.selection()
        if not selecao:
            return
        item_id = int(selecao[0])
        produtos = repo.listar_produtos()
        prod = next((p for p in produtos if p["id"] == item_id), None)
        
        if prod:
            id_produto_selecionado.set(prod["id"])
            entry_nome_prod.delete(0, tk.END)
            entry_nome_prod.insert(0, prod["nome"])
            
            entry_preco_prod.delete(0, tk.END)
            # Converte centavos para formato decimal legível na edição
            entry_preco_prod.insert(0, f"{prod['preco_centavos'] / 100:.2f}".replace(".", ","))
            
            lbl_modo_prod.configure(text=f"Modo: Editando Produto ID {prod['id']}", foreground="darkorange")
            aviso_produtos.configure(text="Altere os campos e clique em Salvar ou clique em Novo.", foreground="black")

    tabela_produtos.bind("<<TreeviewSelect>>", ao_selecionar_produto)

    def salvar_produto():
        """Executa Inclusão (se nenhum ID selecionado) ou Atualização (se ID ativo)."""
        nome = entry_nome_prod.get()
        preco_txt = entry_preco_prod.get()
        id_atual = id_produto_selecionado.get()

        try:
            if id_atual == 0:
                # Inclusão
                novo_id = repo.adicionar_produto(nome, preco_txt)
                messagebox.showinfo("Sucesso", f"Produto cadastrado com sucesso (ID: {novo_id}).")
            else:
                # Edição por ID (mantém a identidade)
                repo.editar_produto(id_atual, nome, preco_txt)
                messagebox.showinfo("Sucesso", f"Produto ID {id_atual} atualizado com sucesso.")
            
            atualizar_listagem_produtos()
            limpar_formulario_produtos()
        except Exception as e:
            messagebox.showerror("Erro de Operação", f"Não foi possível salvar o produto:\n{e}")
            aviso_produtos.configure(text=f"Erro: {e}", foreground="red")

    def excluir_produto_selecionado():
        """Exclui o produto selecionado após confirmação explícita."""
        id_atual = id_produto_selecionado.get()
        if id_atual == 0:
            messagebox.showwarning("Aviso", "Selecione um produto na tabela para excluir.")
            return
        
        confirmado = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o produto ID {id_atual}?")
        if confirmado:
            try:
                repo.excluir_produto(id_atual, confirmado=True)
                messagebox.showinfo("Excluído", f"Produto ID {id_atual} removido com sucesso.")
                atualizar_listagem_produtos()
                limpar_formulario_produtos()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir:\n{e}")

    # Botões de Ação de Produtos
    frame_botoes_prod = ttk.Frame(aba_produtos)
    frame_botoes_prod.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(6, 0))
    frame_botoes_prod.columnconfigure((0, 1, 2), weight=1)

    ttk.Button(frame_botoes_prod, text="Salvar", command=salvar_produto).grid(row=0, column=0, sticky="ew", padx=2)
    ttk.Button(frame_botoes_prod, text="Novo", command=limpar_formulario_produtos).grid(row=0, column=1, sticky="ew", padx=2)
    ttk.Button(frame_botoes_prod, text="Excluir", command=excluir_produto_selecionado).grid(row=0, column=2, sticky="ew", padx=2)

    atualizar_listagem_produtos()

    # ----------------------------------------------------
    # ABA 2: CLIENTES (INÍCIO E LISTAGEM)
    # ----------------------------------------------------
    aba_clientes = ttk.Frame(notebook, padding=12)
    aba_clientes.columnconfigure(1, weight=1)
    aba_clientes.rowconfigure(2, weight=1)
    notebook.add(aba_clientes, text=" Gestão de Clientes ")

    ttk.Label(aba_clientes, text="Nome do Cliente:").grid(row=0, column=0, sticky="w", pady=4)
    entry_nome_cli = ttk.Entry(aba_clientes)
    entry_nome_cli.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=4)

    # Tabela de Clientes
    colunas_cli = ("id", "nome")
    tabela_clientes = ttk.Treeview(aba_clientes, columns=colunas_cli, show="headings", height=8)
    tabela_clientes.heading("id", text="ID")
    tabela_clientes.heading("nome", text="Nome do Cliente")
    tabela_clientes.column("id", width=60, anchor="center")
    tabela_clientes.column("nome", width=380, anchor="w")
    tabela_clientes.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=6)

    def atualizar_listagem_clientes():
        for item in tabela_clientes.get_children():
            tabela_clientes.delete(item)
        for cli in repo.listar_clientes():
            tabela_clientes.insert("", "end", iid=cli["id"], values=(cli["id"], cli["nome"]))

    def salvar_cliente():
        nome = entry_nome_cli.get()
        try:
            repo.adicionar_cliente(nome)
            atualizar_listagem_clientes()
            entry_nome_cli.delete(0, tk.END)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível cadastrar o cliente:\n{e}")

    ttk.Button(aba_clientes, text="Cadastrar Cliente", command=salvar_cliente).grid(row=1, column=0, columnspan=2, sticky="ew", pady=4)

    atualizar_listagem_clientes()

    # Rodapé de Acessibilidade / Teclado
    ttk.Label(
        base, 
        text="Use Tab/Shift+Tab para navegar. Pressione Enter para acionar os botões.", 
        font=("Arial", 8), 
        foreground="gray"
    ).grid(row=2, column=0, sticky="w", pady=(8, 0))

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()
