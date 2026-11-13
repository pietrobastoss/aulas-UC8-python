# A17: assinaturas de apoio; traga sua implementação anterior.

from pathlib import Path
import json
import os
import tempfile

def validar_catalogo(dados):
    """Valida a estrutura do catálogo contido nos dados JSON (deve conter chaves para produtos e clientes válidos)."""
    if not isinstance(dados, dict):
        raise ValueError("O catálogo deve ser um dicionário estruturado.")
    
    # Valida a seção de produtos, se presente
    if "produtos" in dados:
        if not isinstance(dados["produtos"], list):
            raise ValueError("A lista de produtos no catálogo deve ser uma lista.")
        for p in dados["produtos"]:
            if not isinstance(p, dict) or not all(k in p for k in ("id", "nome", "preco_centavos")):
                raise ValueError("Cada produto no catálogo deve possuir id, nome e preco_centavos.")
            if not str(p["nome"]).strip():
                raise ValueError("O nome do produto não pode estar vazio.")
            if int(p["preco_centavos"]) < 0:
                raise ValueError("O preço do produto não pode ser negativo.")

    # Valida a seção de clientes, se presente
    if "clientes" in dados:
        if not isinstance(dados["clientes"], list):
            raise ValueError("A lista de clientes no catálogo deve ser uma lista.")
        for c in dados["clientes"]:
            if not isinstance(c, dict) or not all(k in c for k in ("id", "nome")):
                raise ValueError("Cada cliente no catálogo deve possuir id e nome.")
            if not str(c["nome"]).strip():
                raise ValueError("O nome do cliente não pode estar vazio.")

    return True

def ler_catalogo(caminho):
    """Lê, decodifica e valida o catálogo a partir de um arquivo JSON localizado no caminho especificado."""
    path = Path(caminho)
    if not path.exists():
        # Retorna uma estrutura padrão vazia caso o arquivo ainda não exista
        return {"produtos": [], "clientes": []}

    try:
        with open(path, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError("O arquivo JSON do catálogo está corrompido ou mal formatado.") from e

    validar_catalogo(dados)
    return dados

def salvar_catalogo(caminho, dados):
    """Salva os dados do catálogo em formato JSON de forma atômica utilizando um arquivo temporário."""
    validar_catalogo(dados)
    
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Gravação atômica via arquivo temporário no mesmo diretório
    dir_destino = path.parent
    fd, temp_path = tempfile.mkstemp(dir=dir_destino, text=True)
    
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
            
        # Substitui o arquivo final somente após o sucesso total da escrita
        os.replace(temp_path, path)
        return True
        
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise RuntimeError(f"Erro ao salvar o arquivo do catálogo: {e}") from e