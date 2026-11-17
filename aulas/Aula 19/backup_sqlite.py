# A19: assinaturas de apoio; traga sua implementação anterior.
from contextlib import closing
from pathlib import Path
import sqlite3

def criar_backup(origem, destino):
    """Cria um backup seguro de um banco SQLite utilizando a API de conexão."""
    origem_path = Path(origem)
    destino_path = Path(destino)
    
    if not origem_path.exists():
        raise FileNotFoundError("Arquivo de origem não encontrado.")
    if destino_path.exists():
        raise FileExistsError("O arquivo de destino já existe. Não é permitido sobrescrever.")
        
    with sqlite3.connect(origem_path) as conn_origem, sqlite3.connect(destino_path) as conn_destino:
        conn_origem.backup(conn_destino)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        criar_backup(sys.argv[1], sys.argv[2])
        print(f"Backup de '{sys.argv[1]}' gerado com sucesso em '{sys.argv[2]}'.")
    else:
        print("Uso: python backup_sqlite.py <origem.db> <destino.db>")