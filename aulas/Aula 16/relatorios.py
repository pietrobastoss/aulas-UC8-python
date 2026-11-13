# A16: assinaturas de apoio; traga sua implementação anterior.

from pathlib import Path
import csv
import os
import tempfile

def exportar_csv(caminho, comprovante):
    """Exporta os dados detalhados de um comprovante de pedido confirmado para um arquivo CSV estruturado."""
    if not isinstance(comprovante, dict):
        raise ValueError("O comprovante informado deve ser um dicionário válido.")
    
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Gravação atômica utilizando arquivo temporário no mesmo diretório de destino
    dir_destino = path.parent
    fd, temp_path = tempfile.mkstemp(dir=dir_destino, text=True)
    
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            escritor = csv.writer(f, delimiter=';')
            
            # Cabeçalho do relatório com informações gerais do pagamento
            forma_pagamento = comprovante.get("forma", "Não informada")
            total_centavos = comprovante.get("total_centavos", 0)
            
            escritor.writerow(["COMPROVANTE DE PEDIDO"])
            escritor.writerow(["Forma de Pagamento", forma_pagamento])
            escritor.writerow(["Total Geral (Centavos)", total_centavos])
            escritor.writerow([]) # Linha em branco separadora
            
            # Cabeçalho dos itens do pedido
            escritor.writerow(["Código", "Nome do Produto", "Preço Unitário (Centavos)", "Quantidade", "Subtotal (Centavos)"])
            
            # Escreve cada item listado no comprovante
            itens = comprovante.get("itens", [])
            for item in itens:
                escritor.writerow([
                    item.get("codigo"),
                    item.get("nome"),
                    item.get("preco_unitario"),
                    item.get("quantidade"),
                    item.get("subtotal")
                ])
                
        # Substitui o arquivo final de forma atômica após sucesso na escrita
        os.replace(temp_path, path)
        return True
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise RuntimeError(f"Erro ao exportar o relatório CSV: {e}") from e

