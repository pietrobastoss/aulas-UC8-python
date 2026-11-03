import tkinter as tk
from tkinter import ttk
from pathlib import Path
from aluno import Aluno


def inserir_marca(container, caminho=None):
    # Procura opcionalmente pelo arquivo de imagem ao lado do script usando pathlib
    if caminho is None:
        caminho = Path(__file__).parent / "marca-a06.png"
    else:
        caminho = Path(caminho)

    if caminho.is_file():
        try:
            # Mantém a referência da imagem para evitar que o garbage collector a remova
            container.imagem_marca = tk.PhotoImage(file=str(caminho))
            return ttk.Label(container, image=container.imagem_marca)
        except Exception:
            pass
            
    # Retorna o rótulo textual caso o arquivo de imagem não exista ou falhe
    return ttk.Label(container, text="Sistema escolar fictício — A06")


def abrir_consulta(principal, aluno):
    # Obtém o resumo do aluno confirmado no instante exato da abertura
    texto_resumo = aluno.resumo()
    
    # Se ainda não houver registro confirmado, orienta sem abrir janela vazia
    if "Nenhum" in texto_resumo or not aluno.nome:
        # Você pode usar uma janela de aviso ou o próprio aviso principal; 
        # aqui criamos uma janela informativa rápida ou retornamos.
        janela_aviso = tk.Toplevel(principal)
        janela_aviso.title("Aviso de Consulta")
        janela_aviso.geometry("340x130")
        janela_aviso.transient(principal)
        
        f_aviso = ttk.Frame(janela_aviso, padding=16)
        f_aviso.pack(fill="both", expand=True)
        
        ttk.Label(f_aviso, text="Nenhum registro escolar confirmado ainda.\nConfirme um aluno válido antes de consultar.", justify="center", wraplength=300).pack(pady=(0, 15))
        ttk.Button(f_aviso, text="OK", command=janela_aviso.destroy).pack(anchor="e")
        janela_aviso.bind("<Escape>", lambda event: janela_aviso.destroy())
        return

    # Cria a janela Toplevel de consulta independente (modo retrato / leitura)
    janela_consulta = tk.Toplevel(principal)
    janela_consulta.title("Consulta de Registro Escolar")
    janela_consulta.geometry("420x180")
    janela_consulta.transient(principal)
    
    frame_consulta = ttk.Frame(janela_consulta, padding=16)
    frame_consulta.pack(fill="both", expand=True)
    
    ttk.Label(frame_consulta, text="Retrato do Aluno Confirmado:", font=("", 11, "bold")).pack(anchor="w", pady=(0, 10))
    
    lbl_conteudo = ttk.Label(frame_consulta, text=texto_resumo, wraplength=380, justify="left")
    lbl_conteudo.pack(anchor="w", fill="x", pady=(0, 20))
    
    # Fechamento por botão dedicatório, tecla Escape ou botão 'X' da janela
    btn_fechar = ttk.Button(frame_consulta, text="Fechar", command=janela_consulta.destroy)
    btn_fechar.pack(anchor="e")
    
    janela_consulta.bind("<Escape>", lambda event: janela_consulta.destroy())
    btn_fechar.focus_set()


def criar_janela():
    janela = tk.Tk()
    janela.title("Escolar com consulta — A06")
    janela.columnconfigure(0, weight=1)
    janela.rowconfigure(0, weight=1)

    base = ttk.Frame(janela, padding=12)
    base.grid(row=0, column=0, sticky="nsew")
    base.columnconfigure(0, weight=1)
    base.columnconfigure(1, weight=1)

    # Instância única do modelo criada por janela principal (fora dos callbacks)
    aluno = Aluno()

    # Inserção da marca no topo
    inserir_marca(base).grid(row=0, column=0, columnspan=2, pady=6, sticky="w")

    # Grupos visuais organizados (LabelFrames)
    identificacao = ttk.LabelFrame(base, text="Identificação", padding=10)
    identificacao.grid(row=1, column=0, columnspan=2, sticky="ew", padx=4, pady=6)
    identificacao.columnconfigure(1, weight=1)

    grupo_notas = ttk.LabelFrame(base, text="Notas (0 a 10)", padding=10)
    grupo_notas.grid(row=2, column=0, columnspan=2, sticky="ew", padx=4, pady=6)
    grupo_notas.columnconfigure(1, weight=1)

    acoes = ttk.Frame(base, padding=4)
    acoes.grid(row=3, column=0, columnspan=2, sticky="ew", padx=4, pady=6)
    acoes.columnconfigure(0, weight=1)
    acoes.columnconfigure(1, weight=1)

    # Widgets de identificação
    ttk.Label(identificacao, text="Nome fictício:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
    entrada_nome = ttk.Entry(identificacao)
    entrada_nome.grid(row=0, column=1, padx=6, pady=4, sticky="ew")

    ttk.Label(identificacao, text="Turma fictícia:").grid(row=1, column=0, padx=6, pady=4, sticky="w")
    entrada_turma = ttk.Entry(identificacao)
    entrada_turma.grid(row=1, column=1, padx=6, pady=4, sticky="ew")

    # Widgets dinâmicos para as 5 notas
    entradas_notas = []
    for numero in range(1, 6):
        ttk.Label(grupo_notas, text=f"Nota {numero}:").grid(row=numero, column=0, padx=6, pady=4, sticky="w")
        entrada = ttk.Entry(grupo_notas)
        entrada.grid(row=numero, column=1, padx=6, pady=4, sticky="ew")
        entradas_notas.append(entrada)

    def ao_calcular():
        # Lê os textos diretamente dos Entry (sem validação duplicada na interface)
        nome = entrada_nome.get()
        turma = entrada_turma.get()
        notas_texto = [e.get() for e in entradas_notas]

        # Delega completamente as regras ao modelo
        mensagem = aluno.atualizar(nome, turma, notas_texto)
        aviso.configure(text=mensagem)

        # Atualiza a interface com o resumo oficial gerado pelo modelo
        resultado.configure(text=aluno.resumo())

    def ao_exibir():
        # Aciona a função de consulta passando a janela principal e a instância do aluno
        abrir_consulta(janela, aluno)

    def ao_limpar():
        # Limpa estritamente os campos visuais da interface, mantendo o aluno confirmado intacto
        entrada_nome.delete(0, tk.END)
        entrada_turma.delete(0, tk.END)
        for entrada in entradas_notas:
            entrada.delete(0, tk.END)
        entrada_nome.focus_set()
        aviso.configure(text="Campos limpos. O registro confirmado anteriormente permanece salvo.")

    # Botões de ação alocados no frame dedicado
    ttk.Button(acoes, text="Calcular média", command=ao_calcular).grid(row=0, column=0, padx=4, pady=6, sticky="ew")
    ttk.Button(acoes, text="Consultar", command=ao_exibir).grid(row=0, column=1, padx=4, pady=6, sticky="ew")
    ttk.Button(acoes, text="Limpar campos", command=ao_limpar).grid(row=1, column=0, columnspan=2, padx=4, pady=6, sticky="ew")

    # Rótulos informativos
    aviso = ttk.Label(base, text="Use dados fictícios e confira as cinco notas.", wraplength=430)
    aviso.grid(row=4, column=0, columnspan=2, pady=6, sticky="w")

    resultado = ttk.Label(base, text="Nenhum registro escolar confirmado nesta sessão.", wraplength=430)
    resultado.grid(row=5, column=0, columnspan=2, pady=6, sticky="w")

    entrada_nome.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()