# A13: integre sua versão anterior; preserve-a em outra pasta.

from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from modelos import Pedido, Produto
from relatorios import exportar_csv
from perfis import SessaoDemo


def criar_janela():
    janela = tk.Tk()
    janela.title("A13 — Pizzaria & Sorveteria (CSV e Perfis)")
    janela.geometry("520x460")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    # Inicializa sessão e pedido de demonstração
    sessao = SessaoDemo()
    pedido = Pedido()

    # Adiciona um item de teste inicial para validação do comprovante (ex: Picolé; edição verão)
    prod_exemplo = Produto("P99", "Picolé; edição verão", 450)
    pedido.adicionar(prod_exemplo, 2)  # Subtotal: 900 centavos (R$ 9,00)

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.rowconfigure(4, weight=1)

    # Rótulo de título e instruções
    ttk.Label(base, text="Controle de Vendas, Comprovante CSV e Sessão", font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

    # Frame de Sessão / Perfil
    frame_perfil = ttk.LabelFrame(base, text=" Simulação de Identificação e Perfil ", padding=10)
    frame_perfil.grid(row=1, column=0, sticky="nsew", pady=6)
    frame_perfil.columnconfigure(1, weight=1)

    ttk.Label(frame_perfil, text="Usuário:").grid(row=0, column=0, sticky="w", padx=4)
    entry_nome = ttk.Entry(frame_perfil)
    entry_nome.insert(0, "Operador Caixa")
    entry_nome.grid(row=0, column=1, sticky="ew", padx=4)

    ttk.Label(frame_perfil, text="Perfil:").grid(row=1, column=0, sticky="w", padx=4, pady=4)
    combo_perfil = ttk.Combobox(frame_perfil, values=["Caixa", "Administração"], state="readonly")
    combo_perfil.set("Caixa")
    combo_perfil.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

    lbl_status_sessao = ttk.Label(frame_perfil, text="Sessão: Desconectada", foreground="gray")
    lbl_status_sessao.grid(row=2, column=0, columnspan=2, sticky="w", padx=4, pady=4)

    def acao_entrar():
        nome = entry_nome.get()
        perfil = combo_perfil.get()
        try:
            sessao.entrar(nome, perfil)
            config_status = "Sim (Admin)" if sessao.pode_configurar() else "Não (Caixa)"
            lbl_status_sessao.configure(text=f"Sessão Ativa: {sessao.nome} ({sessao.perfil}) | Pode configurar: {config_status}", foreground="green")
            aviso.configure(text=f"Entrada realizada como {sessao.perfil}.")
        except ValueError as e:
            messagebox.showerror("Erro na Sessão", str(e))

    def acao_sair():
        sessao.sair()
        lbl_status_sessao.configure(text="Sessão: Desconectada", foreground="gray")
        aviso.configure(text="Sessão encerrada com segurança.")

    frame_botoes_sessao = ttk.Frame(frame_perfil)
    frame_botoes_sessao.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(4, 0))
    ttk.Button(frame_botoes_sessao, text="Entrar na Sessão", command=acao_entrar).pack(side="left", padx=2)
    ttk.Button(frame_botoes_sessao, text="Sair", command=acao_sair).pack(side="left", padx=2)

    # Frame de Ações do Pedido e Exportação CSV
    frame_exportacao = ttk.LabelFrame(base, text=" Operações e Exportação CSV ", padding=10)
    frame_exportacao.grid(row=2, column=0, sticky="nsew", pady=6)
    frame_exportacao.columnconfigure(0, weight=1)

    aviso = ttk.Label(frame_exportacao, text="Pedido pronto com item de teste ('Picolé; edição verão').", wraplength=460)
    aviso.grid(row=0, column=0, sticky="w", pady=4)

    def testar_fluxo():
        """Finaliza o pedido, gera o comprovante oficial e exporta para CSV de forma segura."""
        try:
            # Garante que o pedido está finalizado e possui comprovante
            if pedido.status == "ABERTO":
                pedido.finalizar("PIX", confirmado=True)

            # Abre janela de salvamento de arquivo do Tkinter
            arquivo_destino = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
                title="Exportar Comprovante CSV"
            )

            if not arquivo_destino:
                aviso.configure(text="Exportação cancelada pelo usuário. Pedido preservado.")
                return

            # Executa a exportação atômica
            exportar_csv(arquivo_destino, pedido.comprovante)
            aviso.configure(text=f"Sucesso! Comprovante exportado para: {Path(arquivo_destino).name}")
            messagebox.showinfo("Exportação Concluída", "O relatório CSV foi gerado com sucesso preservando a codificação e as colunas.")

        except Exception as e:
            # Tratamento defensivo de erro sem perda de dados ou estado do pedido
            aviso.configure(text=f"Falha na exportação: {e}")
            messagebox.showerror("Erro ao Exportar", f"Não foi possível salvar o arquivo:\n{e}\n\nO pedido atual permanece intacto.")

    ttk.Button(frame_exportacao, text="Finalizar e Exportar Comprovante CSV", command=testar_fluxo).grid(row=1, column=0, sticky="ew", pady=6)

    # Rodapé informativo
    ttk.Label(base, text="Pressione Tab/Shift+Tab para navegar pelos campos e botões.", font=("Arial", 8), foreground="gray").grid(row=5, column=0, sticky="w", pady=(8, 0))

    return janela


if __name__ == "__main__":
    criar_janela().mainloop()