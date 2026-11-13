# A16: integre sua versão anterior; preserve-a em outra pasta.

import tkinter as tk
from tkinter import ttk, messagebox
from repositorio import RepositorioSqlite
from controller import CadastroController

class AplicacaoA16(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A16 — Controllers, Contratos e Clientes")
        self.geometry("640x520")  # Largura x Altura corrigida
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Inicializa o repositório SQLite e o controller de coordenação
        self.repositorio = RepositorioSqlite("dados_a16.db")
        self.controller = CadastroController(self.repositorio)

        # Container principal com Abas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.rowconfigure(0, weight=1)

        # Aba de Produtos
        self.aba_produtos = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.aba_produtos, text="Produtos")
        self.montar_aba_cadastro(self.aba_produtos, tipo="produto")

        # Aba de Clientes
        self.aba_clientes = ttk.Frame(self.notebook, padding=12)
        self.notebook.add(self.aba_clientes, text="Clientes")
        self.montar_aba_cadastro(self.aba_clientes, text_preco=False, tipo="cliente")

    def montar_aba_cadastro(self, aba, text_preco=True, tipo="produto"):
        aba.columnconfigure(0, weight=1)
        aba.rowconfigure(3, weight=1)

        # Rótulo de título da seção
        titulo = "Cadastro de Produtos" if tipo == "produto" else "Cadastro de Clientes"
        ttk.Label(aba, text=titulo, font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Formulário Frame
        form = ttk.LabelFrame(aba, text="Formulário de Ação", padding=10)
        form.grid(row=1, column=0, sticky="ew", pady=(0, 8))
        form.columnconfigure(1, weight=1)

        # ID oculto ou exibido apenas para referência de edição
        id_var = tk.StringVar(value="")
        nome_var = tk.StringVar(value="")
        preco_var = tk.StringVar(value="") if text_preco else None

        # Campos
        ttk.Label(form, text="ID Selecionado:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        lbl_id_val = ttk.Label(form, textvariable=id_var, font=("Segoe UI", 9, "bold"))
        lbl_id_val.grid(row=0, column=1, sticky="w", padx=5, pady=4)

        ttk.Label(form, text="Nome:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        entry_nome = ttk.Entry(form, textvariable=nome_var)
        entry_nome.grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        entry_preco = None
        if text_preco:
            ttk.Label(form, text="Preço (R$):").grid(row=2, column=0, sticky="w", padx=5, pady=4)
            entry_preco = ttk.Entry(form, textvariable=preco_var)
            entry_preco.grid(row=2, column=1, sticky="ew", padx=5, pady=4)

        # Mensagem de Feedback local da aba
        msg_var = tk.StringVar(value="")
        lbl_aviso = ttk.Label(aba, textvariable=msg_var, foreground="#005500")
        lbl_aviso.grid(row=2, column=0, sticky="w", pady=2)

        # Listagem em Treeview
        colunas = ("id", "nome", "preco") if text_preco else ("id", "nome")
        tree = ttk.Treeview(aba, columns=colunas, show="headings", selectmode="browse", height=6)
        tree.heading("id", text="ID")
        tree.column("id", width=50, anchor="center")
        tree.heading("nome", text="Nome")
        tree.column("nome", width=250, anchor="w")
        if text_preco:
            tree.heading("preco", text="Preço (Centavos / R$)")
            tree.column("preco", width=120, anchor="e")

        tree.grid(row=3, column=0, sticky="nsew", pady=4)

        # Barra de rolagem para a tabela
        scrollbar = ttk.Scrollbar(aba, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Funções internas de manipulação de eventos da aba
        def atualizar_lista():
            for item in tree.get_children():
                tree.delete(item)
            try:
                registros = self.controller.listar(tipo)
                for reg in registros:
                    if text_preco:
                        tree.insert("", "end", values=(reg["id"], reg["nome"], reg["preco_centavos"]))
                    else:
                        tree.insert("", "end", values=(reg["id"], reg["nome"]))
            except Exception as e:
                msg_var.set(f"Erro ao carregar listagem: {e}")

        def ao_selecionar(event):
            selecionados = tree.selection()
            if not selecionados:
                return
            valores = tree.item(selecionados[0], "values")
            id_var.set(valores[0])
            nome_var.set(valores[1])
            if text_preco and len(valores) > 2:
                preco_var.set(str(valores[2]))

        tree.bind("<<TreeviewSelect>>", ao_selecionar)

        def limpar_formulario():
            id_var.set("")
            nome_var.set("")
            if text_preco:
                preco_var.set("")
            tree.selection_remove(tree.selection())

        def acao_salvar():
            try:
                codigo = id_var.get().strip() or None
                nome = nome_var.get()
                preco_txt = preco_var.get() if text_preco else ""

                # Delega ao controller a coordenação
                self.controller.salvar(tipo, nome, preco_texto=preco_txt, codigo=codigo)
                
                msg_var.set("Operação realizada com sucesso!")
                limpar_formulario()
                atualizar_lista()
            except Exception as e:
                msg_var.set(f"Erro: {e}")
                messagebox.showerror("Erro ao Salvar", str(e))

        def acao_excluir():
            codigo = id_var.get().strip()
            if not codigo:
                messagebox.showwarning("Aviso", "Selecione um registro na tabela para excluir.")
                return

            confirmado = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o registro ID {codigo}?")
            if not confirmado:
                msg_var.set("Exclusão cancelada pelo usuário.")
                return

            try:
                self.controller.excluir(tipo, codigo, confirmado=True)
                msg_var.set("Registro excluído com sucesso.")
                limpar_formulario()
                atualizar_lista()
            except Exception as e:
                msg_var.set(f"Erro ao excluir: {e}")
                messagebox.showerror("Erro", str(e))

        # Botões de Ação
        botoes = ttk.Frame(aba)
        botoes.grid(row=4, column=0, sticky="ew", pady=8)

        ttk.Button(botoes, text="Salvar / Incluir", command=acao_salvar).pack(side="left", padx=4)
        ttk.Button(botoes, text="Excluir Selecionado", command=acao_excluir).pack(side="left", padx=4)
        ttk.Button(botoes, text="Limpar Campos", command=limpar_formulario).pack(side="left", padx=4)

        # Carga inicial dos dados na tabela
        atualizar_lista()


def criar_janela():
    return AplicacaoA16()


if __name__ == "__main__":
    criar_janela().mainloop()