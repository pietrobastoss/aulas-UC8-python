# A12: assinaturas de apoio; implementação completa do módulo de arquivos e catálogo JSON.
from pathlib import Path
import json
import os
import tempfile

def validar_catalogo(dados):
    """Valida a estrutura completa de um catálogo de produtos carregado via JSON.
       Deve ser uma lista contendo dicionários com chaves: 'id', 'nome', 'preco_centavos'.
       Garante que IDs sejam inteiros positivos únicos, nomes sejam textos válidos 
       e preços sejam inteiros positivos. Retorna True se válido, ou levanta ValueError.
    """
    if not isinstance(dados, list):
        raise ValueError("O catálogo deve ser uma lista de produtos.")
    
    ids_vistos = set()
    for item in dados:
        if not isinstance(item, dict):
            raise ValueError("Cada produto no catálogo deve ser um objeto JSON (dicionário).")
        
        # Verifica chaves obrigatórias
        for chave in ("id", "nome", "preco_centavos"):
            if chave not in item:
                raise ValueError(f"Chave obrigatória ausente no produto: '{chave}'.")
        
        # Validação do ID
        try:
            codigo = int(item["id"])
        except (ValueError, TypeError) as e:
            raise ValueError("O ID do produto deve ser um número inteiro.") from e
            
        if codigo <= 0:
            raise ValueError("O ID do produto deve ser maior que zero.")
            
        if codigo in ids_vistos:
            raise ValueError(f"ID de produto duplicado encontrado: {codigo}.")
        ids_vistos.add(codigo)
        
        # Validação do Nome
        nome = str(item["nome"]).strip()
        if not nome:
            raise ValueError("O nome do produto não pode estar vazio.")
            
        # Validação do Preço em Centavos
        try:
            preco = int(item["preco_centavos"])
        except (ValueError, TypeError) as e:
            raise ValueError("O preço em centavos deve ser um número inteiro.") from e
            
        if preco < 0:
            raise ValueError("O preço em centavos não pode ser negativo.")
            
    return True


def ler_catalogo(caminho):
    """Lê um catálogo de produtos a partir de um arquivo JSON.
       - Se o arquivo não existir, retorna uma lista vazia sem criar arquivo.
       - Se o arquivo contiver JSON inválido ou estrutura inválida, levanta exceção 
         preservando integralmente os bytes originais do arquivo.
    """
    path = Path(caminho)
    if not path.exists():
        return []
    
    # Lê o texto com codificação UTF-8 explícita
    texto = path.read_text(encoding="utf-8")
    
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro de sintaxe no JSON: {e}") from e
        
    # Valida a estrutura de acordo com as regras de negócio do catálogo
    validar_catalogo(dados)
    return dados


def salvar_catalogo(caminho, dados):
    """Salva o catálogo de produtos em um arquivo JSON de forma atômica.
       Valida os dados antes de gravar, escreve em um arquivo temporário no mesmo 
       diretório e só substitui o arquivo de destino ao concluir com sucesso.
    """
    # Valida os dados antes de qualquer escrita
    validar_catalogo(dados)
    
    path = Path(caminho)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Serializa os dados em JSON formatado com UTF-8
    texto = json.dumps(dados, ensure_ascii=False, indent=4)
    
    # Escreve em arquivo temporário no mesmo diretório para garantir atomicidade
    dir_destino = path.parent
    fd, temp_path = tempfile.mkstemp(dir=dir_destino, text=True)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(texto)
        # Substitui o arquivo de destino de forma segura e atômica
        os.replace(temp_path, path)
    except Exception:
        # Garante a remoção do temporário em caso de falha de I/O
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise