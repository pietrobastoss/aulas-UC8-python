# A13: assinaturas de apoio; traga sua implementação anterior.

from pathlib import Path
import csv
import os
import tempfile

def exportar_csv(caminho, comprovante):

    if not isinstance(comprovante, dict) or "itens" not in comprovante:
        raise ValueError("Comprovante inválido ou ausente para exportação.")

    path_obj = Path(caminho)
    diretorio = path_obj.parent
    
    # Valida se a pasta de destino existe e é gravável; caso contrário, lança erro antes de corromper
    try:
        diretorio.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise PermissionError(f"Não foi possível acessar ou criar o diretório de destino: {e}")

    # Extração de dados do comprovante
    forma_pagamento = comprovante.get("forma_pagamento", "Desconhecida")
    total_centavos = comprovante.get("total_centavos", 0)
    total_formatado = comprovante.get("total_formatado", "R$ 0,00")
    itens = comprovante.get("itens", [])

    # Escreve de forma atômica utilizando um arquivo temporário na mesma pasta
    fd, temp_path = tempfile.mkstemp(dir=str(diretorio), prefix="tmp_rel_", text=True)
    try:
        # newline="" evita linhas em branco extras no Windows; encoding="utf-8-sig" adiciona o BOM para o Excel
        with os.fdopen(fd, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            
            # Cabeçalho do relatório
            writer.writerow(["ID", "Nome", "Quantidade", "Preco_Unitario_Centavos", "Subtotal_Centavos", "Forma_Pagamento", "Total_Pedido_Formatado"])
            
            # Linhas de itens
            for item in itens:
                writer.writerow([
                    item.get("codigo", ""),
                    item.get("nome", ""),
                    item.get("quantidade", 0),
                    item.get("preco_unitario_centavos", 0),
                    item.get("subtotal_centavos", 0),
                    forma_pagamento,
                    total_formatado
                ])
                
        # Substituição atômica do arquivo final
        os.replace(temp_path, path_obj)
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        raise RuntimeError(f"Erro ao exportar o relatório CSV: {e}")
    
    return True