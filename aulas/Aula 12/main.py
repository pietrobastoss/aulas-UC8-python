# A12: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
 
# Importação dos módulos da aplicação
import modelos
import arquivos
import pagamento
 
 
class AplicacaoMercado:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("A12 — Mercado: Navegação e Catálogo JSON")
        self.janela.geometry("700x550")
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=1)
 
        # Instância única do pedido para persistir entre as trocas de abas
        self.pedido = modelos.Pedido()
        self.catalogo_atual = []
        self.caminho_arquivo_atual = "catalogo.json"
 
        # Notebook principal para gerenciar as abas
        self.notebook = ttk.Notebook(self.janela)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
 
        # Criação das abas
        self.aba_pedido = ttk.Frame(self.notebook, padding=12)
        self.aba_json = ttk.Frame(self.notebook, padding=12)
 
        self.notebook.add(self.aba_pedido, text="🛒 Pedido e Carrinho")
        self.notebook.add(self.aba_json, text="📂 Exercício JSON / Catálogo")
 
        # Configuração de layout de cada aba
        self.aba_pedido.columnconfigure(0, weight=1)
        self.aba_pedido.rowconfigure(2, weight=1)
        
        self.aba_json.columnconfigure(0, weight=1)
        self.aba_json.rowconfigure(2, weight=1)
 
        # Constrói o conteúdo das abas
        self.construir_aba_pedido()
        self.construir_aba_json()
 
    # -------------------------------------------------------------------------
    # Aba 1: Pedido e Carrinho
    # -------------------------------------------------------------------------
    def construir_aba_pedido(self):
        lbl_titulo = ttk.Label(self.aba_pedido, text="Montagem do Pedido Atual", font=("Arial", 12, "bold"))
        lbl_titulo.grid(row=0, column=0, sticky="w", pady=(0, 8))
 
        frame_controles = ttk.LabelFrame(self.aba_pedido, text="Adicionar Produto de Teste", padding=10)
        frame_controles.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        frame_controles.columnconfigure(3, weight=1)
 
        ttk.Label(frame_controles, text="ID:").grid(row=0, column=0, sticky="w", padx=5)
        self.txt_prod_id = ttk.Entry(frame_controles, width=8)
        self.txt_prod_id.insert(0, "1")
        self.txt_prod_id.grid(row=0, column=1, sticky="w", padx=5)
 
        ttk.Label(frame_controles, text="Nome:").grid(row=0, column=2, sticky="w", padx=5)
        self.txt_prod_nome = ttk.Entry(frame_controles, width=18)
        self.txt_prod_nome.insert(0, "Água com Gás")
        self.txt_prod_nome.grid(row=0, column=3, sticky="ew", padx=5)
 
        ttk.Label(frame_controles, text="Preço (R$):").grid(row=0, column=4, sticky="w", padx=5)
        self.txt_prod_preco = ttk.Entry(frame_controles, width=8)
        self.txt_prod_preco.insert(0, "3,50")
        self.txt_prod_preco.grid(row=0, column=5, sticky="w", padx=5)
 
        ttk.Label(frame_controles, text="Qtd:").grid(row=0, column=6, sticky="w", padx=5)
        self.txt_prod_qtd = ttk.Entry(frame_controles, width=5)
        self.txt_prod_qtd.insert(0, "2")
        self.txt_prod_qtd.grid(row=0, column=7, sticky="w", padx=5)
 
        btn_adicionar = ttk.Button(frame_controles, text="Adicionar ao Pedido", command=self.acao_adicionar_item)
        btn_adicionar.grid(row=0, column=8, padx=10)
 
        # Listagem do carrinho (Treeview)
        colunas = ("codigo", "nome", "preco", "quantidade", "subtotal")
        self.tree_carrinho = ttk.Treeview(self.aba_pedido, columns=colunas, show="headings", height=8)
        self.tree_carrinho.heading("codigo", text="Código")
        self.tree_carrinho.heading("nome", text="Nome do Produto")
        self.tree_carrinho.heading("preco", text="Preço Unit.")
        self.tree_carrinho.heading("quantidade", text="Qtd")
        self.tree_carrinho.heading("subtotal", text="Subtotal")
        
        self.tree_carrinho.column("codigo", width=70, anchor="center")
        self.tree_carrinho.column("nome", width=220, anchor="w")
        self.tree_carrinho.column("preco", width=100, anchor="e")
        self.tree_carrinho.column("quantidade", width=60, anchor="center")
        self.tree_carrinho.column("subtotal", width=110, anchor="e")
        
        self.tree_carrinho.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
 
        frame_rodape = ttk.Frame(self.aba_pedido)
        frame_rodape.grid(row=3, column=0, sticky="ew")
        frame_rodape.columnconfigure(0, weight=1)
 
        self.lbl_total = ttk.Label(frame_rodape, text="Total do Pedido: R$ 0,00", font=("Arial", 11, "bold"))
        self.lbl_total.grid(row=0, column=0, sticky="w")
 
        btn_limpar = ttk.Button(frame_rodape, text="Novo Pedido", command=self.acao_novo_pedido)
        btn_limpar.grid(row=0, column=1, padx=5)
 
        self.atualizar_tabela_carrinho()
 
    def acao_adicionar_item(self):
        try:
            txt_id = self.txt_prod_id.get().strip()
            nome = self.txt_prod_nome.get().strip()
            txt_preco = self.txt_prod_preco.get().strip()
            txt_qtd = self.txt_prod_qtd.get().strip()
 
            if not txt_id or not nome or not txt_preco or not txt_qtd:
                raise ValueError("Preencha todos os campos do produto de teste.")
 
            codigo = int(txt_id)
            
        
            preco_centavos = pagamento.preco_para_centavos(txt_preco)
 
            # Instancia o produto passando o valor em centavos correto
            produto = modelos.Produto(codigo, nome, preco_centavos)
            
            # Adiciona ao pedido
            self.pedido.adicionar(produto, txt_qtd)
            
            # Atualiza a tabela na tela imediatamente
            self.atualizar_tabela_carrinho()
            
        except Exception as e:
            messagebox.showerror("Erro ao adicionar", f"Não foi possível lançar o item:\n{e}")
 
    def atualizar_tabela_carrinho(self):
        # Limpa a tabela atual
        for item in self.tree_carrinho.get_children():
            self.tree_carrinho.delete(item)
 
        # Insere cada linha obtida do modelo de dados
        for linha in self.pedido.linhas():
            # Convertemos explicitamente os valores para garantir que a formatação receba o inteiro correto
            preco_formatado = modelos.formatar(linha["preco_unitario"])
            subtotal_formatado = modelos.formatar(linha["subtotal"])
 
            self.tree_carrinho.insert("", "end", values=(
                linha["codigo"],
                linha["nome"],
                preco_formatado,
                linha["quantidade"],
                subtotal_formatado
            ))
 
        total_cent = self.pedido.total_centavos()
        self.lbl_total.configure(text=f"Total do Pedido: {modelos.formatar(total_cent)}")
 
    def acao_novo_pedido(self):
        if messagebox.askyesno("Confirmar", "Deseja limpar e iniciar um novo pedido?"):
            self.pedido.novo()
            self.atualizar_tabela_carrinho()
            messagebox.showinfo("Novo Pedido", "Carrinho reiniciado com sucesso.")
 
    # -------------------------------------------------------------------------
    # Aba 2: Exercício JSON / Catálogo
    # -------------------------------------------------------------------------
    def construir_aba_json(self):
        lbl_titulo = ttk.Label(self.aba_json, text="Gerenciamento de Catálogo JSON", font=("Arial", 12, "bold"))
        lbl_titulo.grid(row=0, column=0, sticky="w", pady=(0, 8))
 
        frame_botoes = ttk.Frame(self.aba_json)
        frame_botoes.grid(row=1, column=0, sticky="ew", pady=(0, 10))
 
        btn_carregar = ttk.Button(frame_botoes, text="Carregar Catálogo JSON...", command=self.acao_carregar_catalogo)
        btn_carregar.pack(side="left", padx=(0, 8))
 
        btn_salvar = ttk.Button(frame_botoes, text="Salvar Catálogo Exemplo...", command=self.acao_salvar_catalogo)
        btn_salvar.pack(side="left")
 
        self.txt_json_conteudo = tk.Text(self.aba_json, wrap="word", height=15, font=("Consolas", 10))
        self.txt_json_conteudo.grid(row=2, column=0, sticky="nsew", pady=(0, 8))
 
        self.lbl_status_json = ttk.Label(self.aba_json, text="Pronto. Use os botões acima para testar arquivos JSON.", foreground="gray")
        self.lbl_status_json.grid(row=3, column=0, sticky="w")
 
    def acao_carregar_catalogo(self):
        caminho = filedialog.askopenfilename(
            title="Selecione o catálogo JSON",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if not caminho:
            self.lbl_status_json.configure(text="Ação de carregar cancelada pelo usuário.", foreground="blue")
            return
 
        try:
            dados = arquivos.ler_catalogo(caminho)
            self.catalogo_atual = dados
            self.caminho_arquivo_atual = caminho
 
            import json
            texto_formatado = json.dumps(dados, ensure_ascii=False, indent=4)
            self.txt_json_conteudo.delete("1.0", tk.END)
            self.txt_json_conteudo.insert("1.0", texto_formatado)
 
            self.lbl_status_json.configure(text=f"Sucesso: Catálogo carregado de '{Path(caminho).name}'.", foreground="green")
            messagebox.showinfo("Sucesso", f"Catálogo carregado com {len(dados)} produtos!")
            
        except ValueError as e:
            self.lbl_status_json.configure(text=f"Erro de validação/leitura: {e}", foreground="red")
            messagebox.showerror("Erro no Catálogo", f"Não foi possível carregar o arquivo:\n{e}\n\nO arquivo original foi preservado.")
        except Exception as e:
            self.lbl_status_json.configure(text=f"Erro inesperado: {e}", foreground="red")
            messagebox.showerror("Erro", str(e))
 
    def acao_salvar_catalogo(self):
        caminho = filedialog.asksaveasfilename(
            title="Salvar catálogo JSON",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json")]
        )
        if not caminho:
            return
 
        dados_exemplo = [
            {"id": 1, "nome": "Picolé de Limão", "preco_centavos": 450},
            {"id": 2, "nome": "Açaí Tradicional", "preco_centavos": 1200},
            {"id": 3, "nome": "Água Mineral 500ml", "preco_centavos": 300}
        ]
 
        try:
            arquivos.salvar_catalogo(caminho, dados_exemplo)
            self.lbl_status_json.configure(text=f"Catálogo salvo com sucesso em '{Path(caminho).name}'.", foreground="green")
            messagebox.showinfo("Sucesso", "Arquivo de catálogo salvo com segurança!")
        except Exception as e:
            self.lbl_status_json.configure(text=f"Erro ao salvar: {e}", foreground="red")
            messagebox.showerror("Erro", str(e))
 
 
def criar_janela():
    janela = tk.Tk()
    app = AplicacaoMercado(janela)
    return janela
 
 
if __name__ == "__main__":
    criar_janela().mainloop()