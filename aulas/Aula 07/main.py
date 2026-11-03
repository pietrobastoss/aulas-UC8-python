# A07: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk
from modelos import Produto, Item, Pedido, quantidade, formatar

def criar_janela():
    janela = tk.Tk()
    janela.title("A07 — Sorveteria: Produtos, Itens e Pedido")
    janela.geometry("520x560")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    # Catálogo de produtos fictícios conforme o desafio (fruta a 500 e leite a 750, mais um extra)
    catalogo = {
        101: Produto(101, "Fruta", 500),
        102: Produto(102, "Leite", 750),
        103: Produto(103, "Chocolate", 300)
    }

    # Instância única do Pedido atual para esta janela
    pedido_atual = Pedido()

    # Frame principal
    base = ttk.Frame(janela, padding=16)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(4, weight=1)

    # 1. Seção do Catálogo (Combobox Readonly)
    ttk.Label(base, text="Selecione o Produto:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 4))
    
    # Mapeia as opções para exibir de forma legível na interface
    opcoes_catalogo = [f"[{p.codigo}] {p.nome} - {formatar(p.preco_centavos)}" for p in catalogo.values()]
    
    combo_produto = ttk.Combobox(base, values=opcoes_catalogo, state="readonly", width=45)
    combo_produto.grid(row=1, column=0, sticky="ew", pady=(0, 12))
    if opcoes_catalogo:
        combo_produto.current(0) # Seleciona a primeira opção por padrão

    # 2. Seção de Quantidade
    frame_qtd = ttk.Frame(base)
    frame_qtd.grid(row=2, column=0, sticky="ew", pady=(0, 12))
    frame_qtd.columnconfigure(1, weight=1)

    ttk.Label(frame_qtd, text="Quantidade:").grid(row=0, column=0, sticky="w", padx=(0, 8))
    
    entry_quantidade = ttk.Entry(frame_qtd, width=15)
    entry_quantidade.grid(row=0, column=1, sticky="w")
    entry_quantidade.insert(0, "1") # Valor inicial padrão

    # 3. Botão de Ação (Adicionar)
    def adicionar_ao_pedido():
        # Verifica se há seleção no combobox
        selecao_texto = combo_produto.get()
        if not selecao_texto:
            aviso.configure(text="Erro: Selecione um produto no catálogo.", foreground="red")
            return

        # Extrai o código do produto com segurança a partir do formato "[Código] Nome - Preço"
        try:
            codigo_str = selecao_texto.split("]")[0].replace("[", "").strip()
            codigo_produto = int(codigo_str)
        except (ValueError, IndexError):
            aviso.configure(text="Erro: Não foi possível identificar o código do produto.", foreground="red")
            return

        produto_escolhido = catalogo.get(codigo_produto)
        if not produto_escolhido:
            aviso.configure(text="Erro: Produto não encontrado no catálogo.", foreground="red")
            return

        texto_qtd = entry_quantidade.get()

        try:
            # Tenta adicionar ao pedido (o modelo valida a quantidade e lida com códigos repetidos)
            pedido_atual.adicionar(produto_escolhido, texto_qtd)
            
            # Sucesso: Atualiza listagem e total somente após a operação ser aceita
            atualizar_listagem()
            aviso.configure(text=f"Sucesso: {produto_escolhido.nome} adicionado(a) ao pedido!", foreground="green")
            
            # Redefine o campo de quantidade para o padrão e foca nele
            entry_quantidade.delete(0, tk.END)
            entry_quantidade.insert(0, "1")
            entry_quantidade.focus()

        except ValueError as e:
            # Erro de validação ou limite: exibe o erro e PRESERVA os itens anteriores intactos
            aviso.configure(text=f"Erro de validação: {e}", foreground="red")

    btn_adicionar = ttk.Button(base, text="Adicionar ao Pedido", command=adicionar_ao_pedido)
    btn_adicionar.grid(row=3, column=0, sticky="ew", pady=(0, 16))

    # 4. Listagem de Itens (Treeview) e Totalizador
    frame_lista = ttk.Frame(base)
    frame_lista.grid(row=4, column=0, sticky="nsew", pady=(0, 12))
    frame_lista.columnconfigure(0, weight=1)
    frame_lista.rowconfigure(0, weight=1)

    colunas = ("codigo", "nome", "preco", "quantidade", "subtotal")
    tree_itens = ttk.Treeview(frame_lista, columns=colunas, show="headings", height=6)
    
    tree_itens.heading("codigo", text="Cód")
    tree_itens.heading("nome", text="Produto")
    tree_itens.heading("preco", text="Preço Unit.")
    tree_itens.heading("quantidade", text="Qtd")
    tree_itens.heading("subtotal", text="Subtotal")

    tree_itens.column("codigo", width=50, anchor="center")
    tree_itens.column("nome", width=150, anchor="w")
    tree_itens.column("preco", width=80, anchor="e")
    tree_itens.column("quantidade", width=50, anchor="center")
    tree_itens.column("subtotal", width=90, anchor="e")

    tree_itens.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=tree_itens.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree_itens.configure(yscrollcommand=scrollbar.set)

    # Rótulo de Total Geral
    label_total = ttk.Label(base, text="Total do Pedido: R$ 0,00", font=("Arial", 11, "bold"))
    label_total.grid(row=5, column=0, sticky="e", pady=(0, 8))

    # 5. Rótulo de Feedback / Mensagens de Status
    aviso = ttk.Label(base, text="Pronto para iniciar os lançamentos.", wraplength=460, foreground="blue")
    aviso.grid(row=6, column=0, sticky="ew", pady=(4, 0))

    # Função auxiliar para sincronizar a interface com o modelo de dados
    def atualizar_listagem():
        for item_id in tree_itens.get_children():
            tree_itens.delete(item_id)
        
        for linha in pedido_atual.linhas():
            tree_itens.insert("", "end", values=(
                linha["codigo"],
                linha["nome"],
                formatar(linha["preco_unitario"]),
                linha["quantidade"],
                formatar(linha["subtotal"])
            ))
        
        total_centavos = pedido_atual.total_centavos()
        label_total.configure(text=f"Total do Pedido: {formatar(total_centavos)}")

    return janela

if __name__ == "__main__":
    criar_janela().mainloop()