"""A03 — complete a lógica e os callbacks do conversor."""

import tkinter as tk
from tkinter import ttk


def ler_decimal(texto):
    """Trata vírgula como ponto e converte a string para float."""
    texto_limpo = texto.strip().replace(",", ".")
    return float(texto_limpo)


def calcular(campos, registro):
    # 1. Tentar ler os três campos e tratar erro de conversão
    try:
        reais = ler_decimal(campos.get("reais", ""))
        cotacao_dolar = ler_decimal(campos.get("cotacao_dolar", ""))
        cotacao_euro = ler_decimal(campos.get("cotacao_euro", ""))
    except ValueError:
        return "Erro: Todos os campos devem conter valores numéricos válidos."

    # 2. Validar regras de negócio
    if reais < 0:
        return "Erro: O valor em reais não pode ser negativo."

    if cotacao_dolar <= 0 or cotacao_euro <= 0:
        return "Erro: As cotações do dólar e do euro devem ser estritamente maiores que zero."

    # 3. Realizar as conversões
    dolares = reais / cotacao_dolar
    euros = reais / cotacao_euro

    # 4. Confirmar entradas e os dois resultados somente após validar tudo
    registro.update(
        {
            "reais": reais,
            "cotacao_dolar": cotacao_dolar,
            "cotacao_euro": cotacao_euro,
            "dolares": dolares,
            "euros": euros,
        }
    )

    return "Conversão realizada e registrada com sucesso."


def exibir(registro):
    # Tratar ausência de conversão confirmada
    if not registro:
        return "Nenhuma conversão confirmada nesta sessão."

    # Consultar somente o registro e formatar entradas/resultados com duas casas
    return (
        f"Última conversão confirmada:\n"
        f"  • Valor: R$ {registro['reais']:.2f}\n"
        f"  • Cotação USD: R$ {registro['cotacao_dolar']} | Resultado: $ {registro['dolares']:.2f}\n"
        f"  • Cotação EUR: R$ {registro['cotacao_euro']} | Resultado: € {registro['euros']:.2f}"
    )


def limpar(campos):
    # Esvaziar os três campos, preservando o registro e resultados anteriores
    campos["reais"] = ""
    campos["cotacao_dolar"] = ""
    campos["cotacao_euro"] = ""


def criar_janela():
    janela = tk.Tk()
    janela.title("Conversor com cotações fictícias — A03")
    janela.columnconfigure(1, weight=1)
    
    campos = {"reais": "", "cotacao_dolar": "", "cotacao_euro": ""}
    registro = {}

    ttk.Label(
        janela,
        text="Cotações fictícias manuais; sem consulta à internet.",
        wraplength=420,
    ).grid(row=0, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    
    ttk.Label(janela, text="Valor em reais (R$):").grid(
        row=1, column=0, padx=12, pady=6, sticky="w"
    )
    entrada_reais = ttk.Entry(janela)
    entrada_reais.grid(row=1, column=1, padx=12, pady=6, sticky="ew")
    
    ttk.Label(janela, text="R$ por 1 USD:").grid(
        row=2, column=0, padx=12, pady=6, sticky="w"
    )
    entrada_dolar = ttk.Entry(janela)
    entrada_dolar.grid(row=2, column=1, padx=12, pady=6, sticky="ew")
    
    ttk.Label(janela, text="R$ por 1 EUR:").grid(
        row=3, column=0, padx=12, pady=6, sticky="w"
    )
    entrada_euro = ttk.Entry(janela)
    entrada_euro.grid(row=3, column=1, padx=12, pady=6, sticky="ew")

    def ao_calcular():
        # Ler os três Entry e sincronizar com o dicionário de campos
        campos["reais"] = entrada_reais.get()
        campos["cotacao_dolar"] = entrada_dolar.get()
        campos["cotacao_euro"] = entrada_euro.get()

        # Executar o cálculo e validação
        mensagem = calcular(campos, registro)
        aviso.configure(text=mensagem)

        # Se a conversão foi bem-sucedida, atualiza o painel de resultados
        if registro:
            resultado.configure(text=exibir(registro))

    def ao_exibir():
        # Consultar somente o registro, sem ler as entradas editáveis
        resultado.configure(text=exibir(registro))
        aviso.configure(text="Exibindo último registro confirmado.")

    def ao_limpar():
        # Esvaziar os campos lógicos e os widgets visuais, mantendo o registro intacto
        limpar(campos)
        entrada_reais.delete(0, tk.END)
        entrada_dolar.delete(0, tk.END)
        entrada_euro.delete(0, tk.END)

        aviso.configure(text="Campos limpos. O registro anterior foi preservado.")
        entrada_reais.focus_set()

    ttk.Button(janela, text="Calcular", command=ao_calcular).grid(
        row=4, column=0, padx=12, pady=8
    )
    ttk.Button(janela, text="Exibir", command=ao_exibir).grid(
        row=4, column=1, padx=12, pady=8
    )
    ttk.Button(janela, text="Limpar campos", command=ao_limpar).grid(
        row=5, column=0, columnspan=2, pady=6
    )
    
    aviso = ttk.Label(
        janela,
        text="Use vírgula ou ponto decimal, sem milhares.",
        wraplength=420,
    )
    aviso.grid(row=6, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    
    resultado = ttk.Label(
        janela,
        text="Nenhuma conversão confirmada nesta sessão.",
        wraplength=420,
    )
    resultado.grid(row=7, column=0, columnspan=2, padx=12, pady=8, sticky="w")
    
    entrada_reais.focus_set()
    return janela


if __name__ == "__main__":
    criar_janela().mainloop()