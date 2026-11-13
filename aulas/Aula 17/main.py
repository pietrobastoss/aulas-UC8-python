# A17: integre sua versão anterior; preserve-a em outra pasta.
# A17: main.py — Interface gráfica principal integrada com SQLite, Controller e Pedidos
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path

from repositorio import RepositorioSqlite
from controller import CadastroController
from modelos import Pedido, Produto
from pagamento import calcular_pagamento, FATORES
from relatorios import exportar_csv

class AppSorveteria:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("A17 — Sorveteria Integrada")
        self.janela.geometry("850x650")
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)

        # Inicializa o repositório SQLite e o controller
        self.caminho_db = Path("dados_a17.db")
        self.repo = RepositorioSqlite(self.caminho_db)
        self.controller = CadastroController(self.repo)

        # Instância lógica do pedido atual
        self.pedido = Pedido()

        # Layout com Abas (Notebook)
        self.notebook = ttk.Notebook(self.janela)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.aba_cadastros = ttk.Frame(self.notebook, padding=10)
        self.aba_pedido = ttk.Frame(self.notebook, padding=10)
        self.aba_vendas = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.aba_cadastros, text="Cadastros (Produtos e Clientes)")
        self.notebook.add(self.aba_pedido, text="Montagem de Pedido")
        self.notebook.add(self.aba_vendas, text="Vendas e Relatórios")

        self._construir_aba_cadastros()
        self._construir_aba_pedido()
        self._construir_aba_vendas()

        self.atualizar_listagens()

    def _construir_aba_cadastros(self):
        self.aba_cadastros.columnconfigure(0, weight=1)
        self.aba_cadastros.columnconfigure(1, weight=1)
        self.aba_cadastros.rowconfigure(1, weight=1)

        # Frame Esquerdo: Produtos
        f_prod = ttk.LabelFrame(self.aba_cadastros, text="Gestão de Produtos", padding=10)
        f_prod.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)
        f_prod.columnconfigure(1, weight=1)

        ttk.Label(f_prod, text="Nome:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_prod_nome = ttk.Entry(f_prod)
        self.ent_prod_nome.grid(row=0, column=1, sticky="ew", pady=2)

        ttk.Label(f_prod, text="Preço (R$):").grid(row=1, column=0, sticky="w", pady=2)
        self.ent_prod_preco = ttk.Entry(f_prod)
        self.ent_prod_preco.grid(row=1, column=1, sticky="ew", pady=2)

        btn_salvar_prod = ttk.Button(f_prod, text="Salvar Produto", command=self.salvar_produto)
        btn_salvar_prod.grid(row=2, column=0, columnspan=2, pady=5)

        # Treeview de Produtos
        self.tree_produtos = ttk.Treeview(f_prod, columns=("id", "nome", "preco"), show="headings", height=12)
        self.tree_produtos.heading("id", text="ID")
        self.tree_produtos.heading("nome", text="Nome")
        self.tree_produtos.heading("preco", text="Preço (¢)")
        self.tree_produtos.column("id", width=40, anchor="center")
        self.tree_produtos.column("nome", width=140)
        self.tree_produtos.column("preco", width=80, anchor="e")
        self.tree_produtos.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=5)
        self.tree_produtos.bind("<<TreeviewSelect>>", self.carregar_produto_selecionado)

        btn_excluir_prod = ttk.Button(f_prod, text="Excluir Produto Selecionado", command=self.excluir_produto)
        btn_excluir_prod.grid(row=4, column=0, columnspan=2, pady=2)

        # Frame Direito: Clientes
        f_cli = ttk.LabelFrame(self.aba_cadastros, text="Gestão de Clientes", padding=10)
        f_cli.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
        f_cli.columnconfigure(1, weight=1)

        ttk.Label(f_cli, text="Nome do Cliente:").grid(row=0, column=0, sticky="w", pady=2)
        self.ent_cli_nome = ttk.Entry(f_cli)
        self.ent_cli_nome.grid(row=0, column=1, sticky="ew", pady=2)

        btn_salvar_cli = ttk.Button(f_cli, text="Salvar Cliente", command=self.salvar_cliente)
        btn_salvar_cli.grid(row=1, column=0, columnspan=2, pady=5)

        # Treeview de Clientes
        self.tree_clientes = ttk.Treeview(f_cli, columns=("id", "nome"), show="headings", height=12)
        self.tree_clientes.heading("id", text="ID")
        self.tree_clientes.heading("nome", text="Nome")
        self.tree_clientes.column("id", width=40, anchor="center")
        self.tree_clientes.column("nome", width=200)
        self.tree_clientes.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=5)
        self.tree_clientes.bind("<<TreeviewSelect>>", self.carregar_cliente_selecionado)

        btn_excluir_cli = ttk.Button(f_cli, text="Excluir Cliente Selecionado", command=self.excluir_cliente)
        btn_excluir_cli.grid(row=3, column=0, columnspan=2, pady=2)

        # Botão geral para recarregar o catálogo do banco
        btn_atualizar = ttk.Button(self.aba_cadastros, text="Atualizar Catálogo / Clientes", command=self.atualizar_listagens)
        btn_atualizar.grid(row=2, column=0, columnspan=2, pady=10)

        self.produto_id_selecionado = None
        self.cliente_id_selecionado = None

    def _construir_aba_pedido(self):
        self.aba_pedido.columnconfigure(0, weight=1)
        self.aba_pedido.rowconfigure(2, weight=1)

        f_topo = ttk.Frame(self.aba_pedido)
        f_topo.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Label(f_topo, text="Cliente ID:").pack(side="left", padx=2)
        self.ent_pedido_cliente_id = ttk.Entry(f_topo, width=8)
        self.ent_pedido_cliente_id.pack(side="left", padx=5)

        ttk.Label(f_topo, text="Produto ID:").pack(side="left", padx=2)
        self.ent_pedido_prod_id = ttk.Entry(f_topo, width=8)
        self.ent_pedido_prod_id.pack(side="left", padx=5)

        ttk.Label(f_topo, text="Qtd:").pack(side="left", padx=2)
        self.ent_pedido_qtd = ttk.Entry(f_topo, width=6)
        self.ent_pedido_qtd.insert(0, "1")
        self.ent_pedido_qtd.pack(side="left", padx=5)

        btn_add = ttk.Button(f_topo, text="Adicionar ao Pedido", command=self.adicionar_item_pedido)
        btn_add.pack(side="left", padx=10)

        # Tabela de Itens do Pedido Atual
        self.tree_pedido = ttk.Treeview(self.aba_pedido, columns=("codigo", "nome", "preco", "qtd", "subtotal"), show="headings")
        self.tree_pedido.heading("codigo", text="Cód")
        self.tree_pedido.heading("nome", text="Produto")
        self.tree_pedido.heading("preco", text="Preço Unit.")
        self.tree_pedido.heading("qtd", text="Qtd")
        self.tree_pedido.heading("subtotal", text="Subtotal")
        self.tree_pedido.grid(row=2, column=0, sticky="nsew", pady=5)

        # Rodapé de Pagamento e Finalização
        f_baixo = ttk.LabelFrame(self.aba_pedido, text="Fechamento e Pagamento", padding=10)
        f_baixo.grid(row=3, column=0, sticky="ew", pady=5)

        ttk.Label(f_baixo, text="Forma de Pagamento:").grid(row=0, column=0, sticky="w", padx=5)
        self.combo_pagamento = ttk.Combobox(f_baixo, values=list(FATORES.keys()), state="readonly")
        self.combo_pagamento.grid(row=0, column=1, padx=5)
        self.combo_pagamento.set("PIX")

        self.lbl_total_pedido = ttk.Label(f_baixo, text="Total: R$ 0,00", font=("Arial", 11, "bold"))
        self.lbl_total_pedido.grid(row=0, column=2, padx=20)

        btn_finalizar = ttk.Button(f_baixo, text="Finalizar e Gravar Venda", command=self.finalizar_venda)
        btn_finalizar.grid(row=0, column=3, padx=10)

        btn_novo_pedido = ttk.Button(f_baixo, text="Novo Pedido / Limpar", command=self.novo_pedido)
        btn_novo_pedido.grid(row=0, column=4, padx=5)

    def _construir_aba_vendas(self):
        self.aba_vendas.columnconfigure(0, weight=1)
        self.aba_vendas.rowconfigure(0, weight=1)

        self.tree_vendas = ttk.Treeview(self.aba_vendas, columns=("id", "cliente", "forma", "total"), show="headings")
        self.tree_vendas.heading("id", text="Venda ID")
        self.tree_vendas.heading("cliente", text="Cliente")
        self.tree_vendas.heading("forma", text="Pagamento")
        self.tree_vendas.heading("total", text="Total (Centavos)")
        self.tree_vendas.grid(row=0, column=0, sticky="nsew", pady=5)

        btn_exportar = ttk.Button(self.aba_vendas, text="Exportar Comprovante Selecionado para CSV", command=self.exportar_venda_csv)
        btn_exportar.grid(row=1, column=0, pady=10)

    def atualizar_listagens(self):
        try:
            # Produtos
            for item in self.tree_produtos.get_children():
                self.tree_produtos.delete(item)
            produtos = self.repo.listar_produtos()
            for p in produtos:
                self.tree_produtos.insert("", "end", values=(p["id"], p["nome"], p["preco_centavos"]))

            # Clientes
            for item in self.tree_clientes.get_children():
                self.tree_clientes.delete(item)
            clientes = self.repo.listar_clientes()
            for c in clientes:
                self.tree_clientes.insert("", "end", values=(c["id"], c["nome"]))

            # Vendas
            for item in self.tree_vendas.get_children():
                self.tree_vendas.delete(item)
            vendas = self.repo.listar_vendas()
            for v in vendas:
                self.tree_vendas.insert("", "end", values=(v["id"], v["cliente_id"], v["forma_pagamento"], v["total_centavos"]))

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar listagens: {e}")

    def salvar_produto(self):
        nome = self.ent_prod_nome.get()
        preco = self.ent_prod_preco.get()
        codigo = self.produto_id_selecionado
        try:
            self.controller.salvar("produto", nome, preco, codigo)
            messagebox.showinfo("Sucesso", "Produto salvo com sucesso!")
            self.ent_prod_nome.delete(0, tk.END)
            self.ent_prod_preco.delete(0, tk.END)
            self.produto_id_selecionado = None
            self.atualizar_listagens()
        except Exception as e:
            messagebox.showerror("Erro de Validação", str(e))

    def carregar_produto_selecionado(self, event):
        selecao = self.tree_produtos.selection()
        if not selecao:
            return
        item = self.tree_produtos.item(selecao[0])
        valores = item["values"]
        self.produto_id_selecionado = valores[0]
        self.ent_prod_nome.delete(0, tk.END)
        self.ent_prod_nome.insert(0, valores[1])
        self.ent_prod_preco.delete(0, tk.END)
        self.ent_prod_preco.insert(0, str(valores[2]))

    def excluir_produto(self):
        if not self.produto_id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este produto?"):
            try:
                self.controller.excluir("produto", self.produto_id_selecionado, confirmado=True)
                messagebox.showinfo("Sucesso", "Produto excluído.")
                self.produto_id_selecionado = None
                self.atualizar_listagens()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def salvar_cliente(self):
        nome = self.ent_cli_nome.get()
        codigo = self.cliente_id_selecionado
        try:
            self.controller.salvar("cliente", nome, codigo=codigo)
            messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
            self.ent_cli_nome.delete(0, tk.END)
            self.cliente_id_selecionado = None
            self.atualizar_listagens()
        except Exception as e:
            messagebox.showerror("Erro de Validação", str(e))

    def carregar_cliente_selecionado(self, event):
        selecao = self.tree_clientes.selection()
        if not selecao:
            return
        item = self.tree_clientes.item(selecao[0])
        valores = item["values"]
        self.cliente_id_selecionado = valores[0]
        self.ent_cli_nome.delete(0, tk.END)
        self.ent_cli_nome.insert(0, valores[1])

    def excluir_cliente(self):
        if not self.cliente_id_selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        if messagebox.askyesno("Confirmação", "Deseja realmente excluir este cliente?"):
            try:
                self.controller.excluir("cliente", self.cliente_id_selecionado, confirmado=True)
                messagebox.showinfo("Sucesso", "Cliente excluído.")
                self.cliente_id_selecionado = None
                self.atualizar_listagens()
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def adicionar_item_pedido(self):
        try:
            prod_id_txt = self.ent_pedido_prod_id.get().strip()
            qtd_txt = self.ent_pedido_qtd.get().strip()
            
            if not prod_id_txt:
                raise ValueError("Informe o ID do produto.")
            
            prod_id = int(prod_id_txt)
            # Busca o produto atual no banco para conferência de preço e existência
            produtos = self.repo.listar_produtos()
            produto_encontrado = next((p for p in produtos if p["id"] == prod_id), None)
            
            if not produto_encontrado:
                raise ValueError(f"Produto ID {prod_id} não encontrado no catálogo.")

            p_obj = Produto(produto_encontrado["id"], produto_encontrado["nome"], produto_encontrado["preco_centavos"])
            self.pedido.adicionar(p_obj, qtd_txt)
            self.atualizar_visualizacao_pedido()
            
        except Exception as e:
            messagebox.showerror("Erro ao Adicionar", str(e))

    def atualizar_visualizacao_pedido(self):
        for item in self.tree_pedido.get_children():
            self.tree_pedido.delete(item)
            
        for linha in self.pedido.linhas():
            self.tree_pedido.insert("", "end", values=(
                linha["codigo"],
                linha["nome"],
                linha["preco_unitario"],
                linha["quantidade"],
                linha["subtotal"]
            ))
            
        total_c = self.pedido.total_centavos()
        self.lbl_total_pedido.config(text=f"Total: R$ {total_c / 100:.2f}".replace('.', ','))

    def finalizar_venda(self):
        try:
            cli_id_txt = self.ent_pedido_cliente_id.get().strip()
            if not cli_id_txt:
                raise ValueError("Informe o ID do cliente responsável pelo pedido.")
            cli_id = int(cli_id_txt)
            
            forma = self.combo_pagamento.get()
            if not forma:
                raise ValueError("Selecione uma forma de pagamento.")

            linhas = self.pedido.linhas()
            if not linhas:
                raise ValueError("O pedido está vazio.")

            # Valida alteração de preços no catálogo antes da confirmação
            produtos_atuais = {p["id"]: p for p in self.repo.listar_produtos()}
            for l in linhas:
                p_atual = produtos_atuais.get(l["codigo"])
                if not p_atual:
                    raise RuntimeError(f"O produto '{l['nome']}' (ID {l['codigo']}) foi removido do catálogo. Revise o pedido.")
                if p_atual["preco_centavos"] != l["preco_unitario"]:
                    raise RuntimeError(f"O preço do produto '{l['nome']}' foi alterado no catálogo. Revise a montagem antes de confirmar.")

            # Registra a venda e os itens juntos na mesma transação atômica do repositório
            self.repo.registrar_venda(cli_id, linhas, forma)
            
            messagebox.showinfo("Sucesso", "Venda gravada e concluída com sucesso!")
            self.pedido.novo()
            self.atualizar_visualizacao_pedido()
            self.atualizar_listagens()
            
        except Exception as e:
            messagebox.showerror("Falha na Gravação", f"A gravação da venda foi cancelada: {e}")

    def novo_pedido(self):
        self.pedido.novo()
        self.atualizar_visualizacao_pedido()
        self.ent_pedido_cliente_id.delete(0, tk.END)
        self.ent_pedido_prod_id.delete(0, tk.END)

    def exportar_venda_csv(self):
        selecao = self.tree_vendas.selection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione uma venda na lista para exportar.")
            return
        item = self.tree_vendas.item(selecao[0])
        venda_id = item["values"][0]
        
        vendas = self.repo.listar_vendas()
        venda_selecionada = next((v for v in vendas if v["id"] == venda_id), None)
        
        if not venda_selecionada:
            messagebox.showerror("Erro", "Venda não encontrada.")
            return

        arquivo_destino = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Arquivos CSV", "*.csv")],
            initialfile=f"comprovante_venda_{venda_id}.csv"
        )
        
        if arquivo_destino:
            try:
                # Monta a estrutura de comprovante exigida pelo relatorio.py
                comprovante = {
                    "forma": venda_selecionada["forma_pagamento"],
                    "total_centavos": venda_selecionada["total_centavos"],
                    "itens": venda_selecionada["itens"]
                }
                exportar_csv(arquivo_destino, comprovante)
                messagebox.showinfo("Sucesso", "Comprovante exportado com sucesso para CSV!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar CSV: {e}")

def criar_janela():
    root = tk.Tk()
    app = AppSorveteria(root)
    return root

if __name__ == "__main__":
    criar_janela().mainloop()