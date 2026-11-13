# A16: assinaturas de apoio; traga sua implementação anterior.

from pathlib import Path
import json
import os
import tempfile

def validar_catalogo(dados):
    """Valida se a estrutura do catálogo carregado possui o formato esperado (dicionário com chaves 'produtos' e 'clientes')."""
    if not isinstance(dados, dict):
        raise ValueError("O catálogo deve ser um dicionário.")
    
    if "produtos" not in dados or "clientes" not in dados:
        raise ValueError("O catálogo deve conter as chaves 'produtos' e 'clientes'.")
    
    if not isinstance(dados["produtos"], list) or not isinstance(dados["clientes"], list):
        raise ValueError("As listas de produtos e clientes devem ser do tipo lista (list).")
    
    # Validação interna de cada produto
    for prod in dados["produtos"]:
        if not isinstance(prod, dict) or not all(k in prod for k in ("codigo", "nome", "preco_centavos")):
            raise ValueError("Cada produto deve conter 'codigo', 'nome' e 'preco_centavos'.")
    
    # Validação interna de cada cliente
    for cli in dados["clientes"]:
        if not isinstance(cli, dict) or not all(k in cli for k in ("codigo", "nome")):
            raise ValueError("Cada cliente deve conter 'codigo' e 'nome'.")

    return True

def ler_catalogo(caminho):
    """Lê e valida o catálogo de um arquivo JSON localizado no caminho especificado."""
    path = Path(caminho)
    if not path.exists():
        # Retorna estrutura padrão vazia se o arquivo ainda não existir
        return {"produtos": [], "clientes": []}
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            conteudo = f.read().strip()
            if not conteudo:
                return {"produtos": [], "clientes": []}
            dados = json.loads(conteudo)
            validar_catalogo(dados)
            return dados
    except json.JSONDecodeError as e:
        raise ValueError("O arquivo JSON contém erros de sintaxe ou codificação inválida.") from e
    except Exception as e:
        raise ValueError(f"Erro ao ler o catálogo: {e}") from e

def salvar_catalogo(caminho, dados):
    """Salva o catálogo em formato JSON utilizando gravação atômica para proteger contra falhas."""
    validar_catalogo(dados)
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Gravação atômica usando arquivo temporário no mesmo diretório
    dir_destino = path.parent
    fd, temp_path = tempfile.mkstemp(dir=dir_destino, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
        # Substitui o arquivo final de forma atômica
        os.replace(temp_path, path)
    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise RuntimeError(f"Erro ao salvar o catálogo: {e}") from e