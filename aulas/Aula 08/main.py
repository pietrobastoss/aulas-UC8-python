# A08: main.py — Sorveteria (Interface Tkinter)
import tkinter as tk
from tkinter import ttk, messagebox
from decimal import Decimal
from modelos import Pedido, Produto, formatar
from pagamento import calcular_pagamento

def criar_janela():
    janela = tk.Tk()
    janela.title("A08 — Sorveteria: Pagamentos e Arredondamento")
    janela.geometry("520x550")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    base = ttk.Frame(janela, padding=16)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(3, weight=1)

    # Pedido de exemplo com um produto de R$ 100,00
    pedido = Pedido()
    sorvete_exemplo = Produto("001", "Sorvete Especial 1L", 10000)
    pedido.adicionar(sorvete_exemplo, "1")

    # Rótulo de título
    ttk.Label(base, text="Cálculo de Pagamento e Prévia", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

    # Frame de seleção de pagamento
    frame_pagamento = ttk.LabelFrame(base, text=" Forma de Pagamento ", padding=12)
    frame_pagamento.grid(row=1, column=0, sticky="ew", pady=8)
    frame_pagamento.columnconfigure(1, weight=1)

    ttk.Label(frame_pagamento, text="Escolha:").grid(row=0, column=0, sticky="w", padx=4)
    
    forma_var = tk.StringVar(value="PIX")
    combo_forma = ttk.Combobox(frame_pagamento, textvariable=forma_var, values=["Dinheiro", "PIX", "Débito", "Crédito 1x"], state="readonly")
    combo_forma.grid(row=0, column=1, sticky="ew", padx=4)

    def acionar_conferencia():
        try:
            subtotal_centavos = pedido.total_centavos()
            subtotal_texto = f"{subtotal_centavos / 100:.2f}"
            forma_escolhida = forma_var.get()

            sub_dec, desc_dec, tot_dec = calcular_pagamento(subtotal_texto, forma_escolhida)

            resultado_texto = (
                f"Forma: {forma_escolhida}\n"
                f"Subtotal: R$ {sub_dec:.2f}\n"
                f"Desconto: R$ {desc_dec:.2f}\n"
                f"Total a Pagar: R$ {tot_dec:.2f}"
            )
            lbl_resultado.configure(text=resultado_texto, foreground="black")
            lbl_aviso.configure(text="Conferência realizada com sucesso. Pedido preservado.", foreground="green")

        except Exception as e:
            messagebox.showerror("Erro no Pagamento", str(e))
            lbl_aviso.configure(text=f"Erro: {e}", foreground="red")

    btn_conferir = ttk.Button(frame_pagamento, text="Conferir pagamento", command=acionar_conferencia)
    btn_conferir.grid(row=0, column=2, padx=4)

    # Frame de resultados e prévia
    frame_resultado = ttk.LabelFrame(base, text=" Prévia da Operação ", padding=12)
    frame_resultado.grid(row=2, column=0, sticky="ew", pady=8)
    frame_resultado.columnconfigure(0, weight=1)

    lbl_resultado = ttk.Label(frame_resultado, text="Nenhuma conferência realizada.", font=("Consolas", 10))
    lbl_resultado.grid(row=0, column=0, sticky="w", padx=4, pady=4)

    # Aviso dinâmico
    lbl_aviso = ttk.Label(base, text="Pronto para conferir.", font=("Segoe UI", 9, "italic"))
    lbl_aviso.grid(row=4, column=0, sticky="w", pady=4)

    return janela

if __name__ == "__main__":
    criar_janela().mainloop()