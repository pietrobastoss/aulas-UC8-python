# A15: assinaturas de apoio; traga sua implementação anterior.

from pathlib import Path
import json
import os
import tempfile

def validar_catalogo(dados):
    """
    Valida a estrutura dos dados do catálogo carregados do JSON.
    Garante que os dados sejam um dicionário contendo listas válidas de itens.
    """
    if not isinstance(dados, dict):
        raise ValueError("O catálogo raiz deve ser um dicionário.")
    
    for chave, lista_itens in dados.items():
        if not isinstance(lista_itens, list):
            raise ValueError(f"A categoria '{chave}' deve ser uma lista de itens.")
        for item in lista_itens:
            if not isinstance(item, dict):
                raise ValueError("Cada item do catálogo deve ser um dicionário.")
            if "codigo" not in item or "nome" not in item or "preco_centavos" not in item:
                raise ValueError("Item do catálogo incompleto: faltam campos obrigatórios.")
    return True


def ler_catalogo(caminho):
    """
    Lê o catálogo de um arquivo JSON localizado no caminho especificado.
    Valida a estrutura antes de retornar os dados.
    """
    path_obj = Path(caminho)
    if not path_obj.exists():
        raise FileNotFoundError(f"Arquivo de catálogo não encontrado: '{caminho}'.")
    
    try:
        with open(path_obj, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao decodificar JSON do catálogo: {e}")
        
    validar_catalogo(dados)
    return dados


def salvar_catalogo(caminho, dados):
    """
    Salva o catálogo em formato JSON de forma atômica, utilizando um arquivo 
    temporário no mesmo diretório para evitar corrupção em caso de falhas.
    """
    validar_catalogo(dados)
    path_obj = Path(caminho)
    diretorio = path_obj.parent
    diretorio.mkdir(parents=True, exist_ok=True)

    # Escrita atômica via arquivo temporário na mesma pasta
    fd, temp_path = tempfile.mkstemp(dir=str(diretorio), prefix="tmp_cat_", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        
        # Substituição atômica do arquivo final
        os.replace(temp_path, path_obj)
    except Exception as e:
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass
        raise RuntimeError(f"Falha ao salvar o catálogo: {e}")
