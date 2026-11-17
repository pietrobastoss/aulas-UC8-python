from pathlib import Path
import os
import sqlite3
from repositorio import RepositorioSqlite
from modelos import Pedido, Produto
from relatorios import exportar_csv
import traceback

def criar_backup(origem_path, destino_path):
    """Cria um backup seguro usando a API nativa de conexão do SQLite."""
    origem_path = Path(origem_path)
    destino_path = Path(destino_path)
    
    if not origem_path.exists():
        raise FileNotFoundError("Arquivo de origem não encontrado.")
    if destino_path.exists():
        raise FileExistsError("O arquivo de destino já existe. Não é permitido sobrescrever.")
        
    with sqlite3.connect(origem_path) as conn_origem, sqlite3.connect(destino_path) as conn_destino:
        conn_origem.backup(conn_destino)

def verificar():
    caminho_db = Path("teste_a20.db")
    caminho_backup = Path("backup_a20.db")
    caminho_csv = Path("teste_comprovante.csv")
    
    # Função auxiliar segura para apagar arquivos travados ou existentes antes de recriar
    def limpar_arquivo(arquivo):
        if arquivo.exists():
            try:
                arquivo.unlink()
            except PermissionError:
                pass

    # Limpeza prévia para garantir substituição limpa
    limpar_arquivo(caminho_db)
    limpar_arquivo(caminho_backup)
    limpar_arquivo(caminho_csv)

    repo = RepositorioSqlite(caminho_db)

    try:
        # 1. Cadastra cliente e produtos de teste
        cli_id = repo.adicionar_cliente("Maria Silva")
        p1_id = repo.adicionar_produto("Sorvete Chocolate", 500)
        p2_id = repo.adicionar_produto("Sorvete Morango", 600)

        # 2. Testa cenário de SUCESSO: Registro de venda e itens juntos
        itens_sucesso = [
            {"codigo": p1_id, "nome": "Sorvete Chocolate", "preco_unitario": 500, "quantidade": 2, "subtotal": 1000},
            {"codigo": p2_id, "nome": "Sorvete Morango", "preco_unitario": 600, "quantidade": 1, "subtotal": 600}
        ]
        venda_id = repo.registrar_venda(cli_id, itens_sucesso, "PIX")
        assert venda_id > 0, "A venda deveria retornar um ID válido."

        vendas_listadas = repo.listar_vendas()
        assert len(vendas_listadas) == 1, "Deveria existir exatamente uma venda registrada."
        assert len(vendas_listadas[0]["itens"]) == 2, "A venda deve conter exatamente 2 itens."

        # 3. Testa FALHA NA TRANSAÇÃO (Rollback / Sem venda parcial)
        itens_falha = [
            {"codigo": p1_id, "nome": "Sorvete Chocolate", "preco_unitario": 500, "quantidade": 1, "subtotal": 500},
            {"codigo": 9999, "nome": "Produto Inexistente", "preco_unitario": 1000, "quantidade": 1, "subtotal": 1000}
        ]
        
        total_vendas_antes = len(repo.listar_vendas())
        try:
            repo.registrar_venda(cli_id, itens_falha, "Dinheiro")
            raise AssertionError("Deveria ter falhado ao registrar item com ID inexistente.")
        except Exception:
            pass

        total_vendas_depois = len(repo.listar_vendas())
        assert total_vendas_antes == total_vendas_depois, "O rollback deve impedir a gravação de venda parcial em caso de falha."

        # 4. Fecha explicitamente a conexão do repositório antes do backup
        if hasattr(repo, "fechar"):
            repo.fechar()
        elif hasattr(repo, "conn") and repo.conn:
            repo.conn.close()
        del repo

        # Testa OBRIGATÓRIO: Validação da API de Backup e Conexão Independente
        criar_backup(caminho_db, caminho_backup)
        assert caminho_backup.exists(), "O arquivo de destino do backup deveria ter sido criado."

        # Consulta a cópia por uma conexão independente
        conn_copia = sqlite3.connect(caminho_backup)
        try:
            cursor = conn_copia.cursor()
            cliente_copia = cursor.execute("SELECT nome FROM clientes WHERE id = ?", (cli_id,)).fetchone()
        finally:
            conn_copia.close()
            
        assert cliente_copia is not None, "A cópia do banco deveria conter o cliente cadastrado."
        assert cliente_copia[0] == "Maria Silva", f"Nome esperado 'Maria Silva', obtido: {cliente_copia[0]}"

        # Testa recusa de sobrescrita (destino já existente)
        try:
            criar_backup(caminho_db, caminho_backup)
            recusou = False
        except FileExistsError:
            recusou = True
        assert recusou, "O sistema deveria recusar sobrescrever um backup existente."

        # 5. Reabre repositório para testar Pedido e CSV
        repo_novo = RepositorioSqlite(caminho_db)
        pedido = Pedido()
        p_obj = Produto(p1_id, "Sorvete Chocolate", 500)
        pedido.adicionar(p_obj, "2")
        
        comprovante = pedido.finalizar("PIX", confirmado=True)
        assert comprovante["total_centavos"] == 870, "O total com desconto PIX deve ser 870 centavos."

        exportar_csv(caminho_csv, comprovante)
        assert caminho_csv.exists(), "O arquivo CSV do comprovante deve ser gerado com sucesso."
        
        if hasattr(repo_novo, "fechar"):
            repo_novo.fechar()
        elif hasattr(repo_novo, "conn") and repo_novo.conn:
            repo_novo.conn.close()
        del repo_novo

        # Limpeza final segura
        limpar_arquivo(caminho_db)
        limpar_arquivo(caminho_backup)
        limpar_arquivo(caminho_csv)

        return True

    except Exception as e:
        print("Erro detalhado durante a verificação:")
        traceback.print_exc()
        try:
            if 'repo' in locals():
                if hasattr(repo, 'fechar'): repo.fechar()
                elif hasattr(repo, 'conn') and repo.conn: repo.conn.close()
            if 'repo_novo' in locals():
                if hasattr(repo_novo, 'fechar'): repo_novo.fechar()
                elif hasattr(repo_novo, 'conn') and repo_novo.conn: repo_novo.conn.close()
        except:
            pass
            
        limpar_arquivo(caminho_db)
        limpar_arquivo(caminho_backup)
        limpar_arquivo(caminho_csv)
        return False

if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")