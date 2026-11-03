# A09: integre sua versão anterior; preserve-a em outra pasta.
import tkinter as tk
from tkinter import ttk, messagebox
from modelos import Pedido, Produto, formatar
from pagamento import calcular_pagamento, FATORES

def criar_janela():
    janela = tk.Tk()
    janela.title("A09 — Catálogo e Carrinho: Seleção por Identidade")
    janela.geometry("750x550")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    # Inicializa o pedido e produtos padrão do catálogo
    pedido = Pedido()
    catalogo_produtos = [
        Produto(codigo=1, nome="Fruta", preco_centavos=1000),
        Produto(codigo=2, nome="Leite", preco_centavos=500),
        Produto(codigo=3, nome="Pão", preco_centavos=300),
    ]

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.columnconfigure(1, weight=1)
    base.rowconfigure(1, weight=1)

    # Título principal
    ttk.Label(base, text="Catálogo e Carrinho — Seleção por Identidade (ID)", font=("Helvetica", 11, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 8), sticky="w")

    # --- FRAME ESQUERDO: Catálogo ---
    frame_cat = ttk.LabelFrame(base, text=" Catálogo de Produtos ", padding=8)
    frame_cat.grid(row=1, column=0, sticky="nsew", padx=(0, 6))
    frame_cat.columnconfigure(0, weight=1)
    frame_cat.rowconfigure(0, weight=1)

    tree_cat = ttk.Treeview(frame_cat, columns=("nome", "preco"), show="headings", selectmode="browse")
    tree_cat.heading("nome", text="Produto")
    tree_cat.heading("preco", text="Preço")
    tree_cat.column("nome", width=120, anchor="w")
    tree_cat.column("preco", width=80, anchor="e")
    tree_cat.grid(row=0, column=0, sticky="nsew")

    scroll_cat = ttk.Scrollbar(frame_cat, orient="vertical", command=tree_cat.yview)
    scroll_cat.grid(row=0, column=1, sticky="ns")
    tree_cat.configure(yscrollcommand=scroll_cat.set)

    # Preenche o catálogo usando o código do produto como iid (Identidade)
    for p in catalogo_produtos:
        tree_cat.insert("", "end", iid=str(p.codigo), values=(p.nome, formatar(p.preco_centavos)))

    # --- FRAME DIREITO: Carrinho ---
    frame_car = ttk.LabelFrame(base, text=" Carrinho de Compras ", padding=8)
    frame_car.grid(row=1, column=1, sticky="nsew", padx=(6, 0))
    frame_car.columnconfigure(0, weight=1)
    frame_car.rowconfigure(0, weight=1)

    tree_car = ttk.Treeview(frame_car, columns=("nome", "preco", "qtd", "subtotal"), show="headings", selectmode="browse")
    tree_car.heading("nome", text="Produto")
    tree_car.heading("preco", text="Preço")
    tree_car.heading("qtd", text="Qtd")
    tree_car.heading("subtotal", text="Subtotal")
    tree_car.column("nome", width=100, anchor="w")
    tree_car.column("preco", width=60, anchor="e")
    tree_car.column("qtd", width=40, anchor="center")
    tree_car.column("subtotal", width=70, anchor="e")
    tree_car.grid(row=0, column=0, sticky="nsew")

    scroll_car = ttk.Scrollbar(frame_car, orient="vertical", command=tree_car.yview)
    scroll_car.grid(row=0, column=1, sticky="ns")
    tree_car.configure(yscrollcommand=scroll_car.set)

    # --- PAINEL DE CONTROLES E AÇÕES ---
    frame_controles = ttk.LabelFrame(base, text=" Ações e Quantidade ", padding=10)
    frame_controles.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 0))
    frame_controles.columnconfigure(3, weight=1)

    ttk.Label(frame_controles, text="Quantidade:").grid(row=0, column=0, sticky="w", padx=4)
    entry_qtd = ttk.Entry(frame_controles, width=8)
    entry_qtd.insert(0, "1")
    entry_qtd.grid(row=0, column=1, sticky="w", padx=4)

    aviso = ttk.Label(frame_controles, text="Pronto para operar.", foreground="blue")
    aviso.grid(row=0, column=2, sticky="w", padx=12)

    # --- PAINEL DE PAGAMENTO E TOTAIS ---
    frame_pagamento = ttk.LabelFrame(base, text=" Resumo e Pagamento ", padding=10)
    frame_pagamento.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
    frame_pagamento.columnconfigure(3, weight=1)

    lbl_total = ttk.Label(frame_pagamento, text="Total: R$ 0,00", font=("Helvetica", 10, "bold"))
    lbl_total.grid(row=0, column=0, sticky="w", padx=4)

    ttk.Label(frame_pagamento, text="Forma:").grid(row=0, column=1, sticky="w", padx=(15, 4))
    combo_forma = ttk.Combobox(frame_pagamento, values=list(FATORES.keys()), state="readonly", width=12)
    combo_forma.set("Crédito 1x")
    combo_forma.grid(row=0, column=2, sticky="w", padx=4)

    lbl_previa = ttk.Label(frame_pagamento, text="Prévia: R$ 0,00", font=("Helvetica", 10, "bold"), foreground="green")
    lbl_previa.grid(row=0, column=3, sticky="e", padx=4)

    # --- FUNÇÕES DE ATUALIZAÇÃO DA TELA ---
    def atualizar_interface():
        # Limpa listagem do carrinho
        for item in tree_car.get_children():
            tree_car.delete(item)

        # Preenche com os dados atuais do modelo
        for linha in pedido.linhas():
            tree_car.insert(
                "", "end", 
                iid=str(linha["codigo"]), 
                values=(linha["nome"], formatar(linha["preco"]), linha["qtd"], formatar(linha["subtotal"]))
            )

        # Atualiza totais monetários
        centavos = pedido.total_centavos()
        subtotal_txt = f"{centavos / 100:.2f}"
        lbl_total.configure(text=f"Total: {formatar(centavos)}")

        try:
            forma_escolhida = combo_forma.get()
            total_calc = calcular_pagamento(subtotal_txt, forma_escolhida)
            lbl_previa.configure(text=f"Prévia: R$ {total_calc:.2f}")
        except Exception:
            lbl_previa.configure(text="Prévia: R$ 0,00")

    # --- CALLBACKS DE AÇÃO ---
    def acao_adicionar():
        selecao = tree_cat.selection()
        if not selecao:
            aviso.configure(text="Selecione um produto no catálogo para adicionar.")
            return
        
        codigo_str = selecao[0]
        produto_alvo = next((p for p in catalogo_produtos if str(p.codigo) == codigo_str), None)
        
        if not produto_alvo:
            aviso.configure(text="Produto selecionado não encontrado.")
            return

        try:
            texto_q = entry_qtd.get()
            pedido.adicionar(produto_alvo, texto_q)
            atualizar_interface()
            aviso.configure(text=f"Produto '{produto_alvo.nome}' adicionado/somado com sucesso.", foreground="green")
        except ValueError as e:
            aviso.configure(text=str(e), foreground="red")

    def acao_atualizar():
        selecao = tree_car.selection()
        if not selecao:
            aviso.configure(text="Selecione um item no carrinho para atualizar.")
            return

        codigo_str = selecao[0]
        try:
            texto_q = entry_qtd.get()
            pedido.atualizar(codigo_str, texto_q)
            atualizar_interface()
            aviso.configure(text=f"Quantidade do código {codigo_str} atualizada com sucesso.", foreground="green")
        except (ValueError, KeyError) as e:
            aviso.configure(text=str(e), foreground="red")

    def acao_remover():
        selecao = tree_car.selection()
        if not selecao:
            aviso.configure(text="Selecione um item no carrinho para remover.")
            return

        codigo_str = selecao[0]
        try:
            pedido.remover(codigo_str)
            atualizar_interface()
            aviso.configure(text=f"Item {codigo_str} removido do carrinho.", foreground="green")
        except KeyError as e:
            aviso.configure(text=str(e), foreground="red")

    # --- BOTÕES DE COMANDO ---
    frame_botoes = ttk.Frame(base)
    frame_botoes.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0))

    ttk.Button(frame_botoes, text="Adicionar ao Carrinho", command=acao_adicionar).pack(side="left", padx=4)
    ttk.Button(frame_botoes, text="Atualizar Quantidade", command=acao_atualizar).pack(side="left", padx=4)
    ttk.Button(frame_botoes, text="Remover Item", command=acao_remover).pack(side="left", padx=4)

    # Vincula alteração da forma de pagamento à reavaliação da prévia
    combo_forma.bind("<<ComboboxSelected>>", lambda e: atualizar_interface())

    atualizar_interface()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()