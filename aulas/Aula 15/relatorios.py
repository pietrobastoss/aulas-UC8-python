# A15: assinaturas de apoio; traga sua implementação anterior.

from pathlib import Path
import csv
import os
import tempfile

def exportar_csv(caminho, comprovante):
    """
    Exporta o comprovante confirmado para um arquivo CSV utilizando codificação UTF-8 com BOM (utf-8-sig)
    e o separador ponto e vírgula (;). Emprega escrita atômica via arquivo temporário
    para evitar perda ou corrupção de dados em caso de falhas.
    """
    if not isinstance(comprovante, dict) or "itens" not in comprovante:
        raise ValueError("Comprovante inválido ou ausente para exportação.")

    path_obj = Path(caminho)
    diretorio = path_obj.parent
    
    # Valida se a pasta de destino existe/pode ser criada
    try:
        diretorio.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise PermissionError(f"Não foi possível acessar ou criar o diretório de destino: {e}")

    # Extração das informações do comprovante
    forma_pagamento = comprovante.get("forma_pagamento", "Desconhecida")
    total_formatado = comprovante.get("total_formatado", "R$ 0,00")
    itens = comprovante.get("itens", [])

    # Escrita atômica via arquivo temporário
    fd, temp_path = tempfile.mkstemp(dir=str(diretorio), prefix="tmp_rel_", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f, delimiter=";")
            
            # Cabeçalho do relatório
            writer.writerow([
                "ID", 
                "Nome", 
                "Quantidade", 
                "Preco_Unitario_Centavos", 
                "Subtotal_Centavos", 
                "Forma_Pagamento", 
                "Total_Pedido_Formatado"
            ])
            
            # Escreve os itens do comprovante
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
                
        # Substituição atômica do arquivo original
        os.replace(temp_path, path_obj)
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        raise RuntimeError(f"Erro ao exportar o relatório CSV: {e}")
    
    return True
