# A17: assinaturas de apoio; traga sua implementação anterior.

import tkinter as tk
from tkinter import ttk, messagebox

def criar_comparacao():
    """Tentei inicializar uma janela utilizando CustomTkinter, 
    deu um  aviso sobre não ter a biblioteca mas  manteve o fluxo funcional.
    """
    try:
        import customtkinter as ctk
        
        # Configuração inicial do CustomTkinter
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        janela = ctk.CTk()
        janela.title("A17 — Comparação CustomTkinter (Opcional)")
        janela.geometry("500x400")
        janela.grid_columnconfigure(0, weight=1)
        
        frame = ctk.CTkFrame(janela, corner_radius=10)
        frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        frame.grid_columnconfigure(0, weight=1)
        
        lbl_titulo = ctk.CTkLabel(frame, text="Demonstração Opcional com CustomTkinter", font=("Arial", 16, "bold"))
        lbl_titulo.grid(row=0, column=0, pady=10)
        
        lbl_info = ctk.CTkLabel(
            frame, 
            text="Esta tela é apenas uma comparação visual opcional.\n"
                 "O núcleo da aplicação (transações SQLite, repositórios, "
                 "controller e modelos) permanece idêntico ao padrão ttk.",
            wraplength=400,
            justify="left"
        )
        lbl_info.grid(row=1, column=0, pady=10)
        
        def acao_teste():
            messagebox.showinfo("CustomTkinter", "Ação executada com sucesso na interface opcional!")
            
        btn_testar = ctk.CTkButton(frame, text="Testar Ação Integrada", command=acao_teste)
        btn_testar.grid(row=2, column=0, pady=20)
        
        return janela
        
    except ImportError:
        # Fallback caso a biblioteca CustomTkinter não esteja instalada no ambiente
        janela = tk.Tk()
        janela.title("A17 — CustomTkinter Indisponível")
        janela.geometry("450x200")
        
        lbl = ttk.Label(
            janela, 
            text="A biblioteca 'customtkinter' não está instalada neste ambiente.\n\n"
                 "Conforme a orientação da Aula 17, isso não bloqueia o núcleo\n"
                 "da aplicação principal baseada em ttk (main.py).", 
            padding=20,
            wraplength=400
        )
        lbl.pack(expand=True, fill="both")
        
        return janela

if __name__ == "__main__":
    criar_comparacao().mainloop()
