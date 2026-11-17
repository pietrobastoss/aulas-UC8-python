from contextlib import closing
import sqlite3

def demonstrar():
    """Demonstra o uso de chaves estrangeiras e a recusa de exclusão de registros vinculados no SQLite."""
    # Cria um banco em memória ou arquivo temporário para a demonstração
    conn = sqlite3.connect(":memory:")
    
    with closing(conn):
        # OBRIGATÓRIO: Ativar chaves estrangeiras no SQLite (por padrão vêm desativadas)
        conn.execute("PRAGMA foreign_keys = ON;")
        
        cursor = conn.cursor()
        
        # Criação das tabelas com relacionamento e restrição de exclusão
        cursor.execute("""
            CREATE TABLE alunos (
                id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL
            );
        """)
        
        cursor.execute("""
            CREATE TABLE matriculas (
                id INTEGER PRIMARY KEY,
                aluno_id INTEGER,
                FOREIGN KEY (aluno_id) REFERENCES alunos (id) ON DELETE RESTRICT
            );
        """)
        
        # Insere dados de teste
        cursor.execute("INSERT INTO alunos (id, nome) VALUES (1, 'Lia');")
        cursor.execute("INSERT INTO matriculas (id, aluno_id) VALUES (101, 1);")
        conn.commit()
        
        print("Aluno e matrícula inseridos com sucesso.")
        
        # Tenta excluir o aluno que possui matrícula ativa (deve disparar IntegrityError)
        exclusao_bloqueada = False
        try:
            cursor.execute("DELETE FROM alunos WHERE id = 1;")
            conn.commit()
        except sqlite3.IntegrityError:
            exclusao_bloqueada = True
            print("Tentativa de exclusão bloqueada com sucesso pela regra ON DELETE RESTRICT.")
            
        return exclusao_bloqueada

if __name__ == "__main__":
    sucesso = demonstrar()
    print("Demonstração concluída. Exclusão vinculada bloqueada:", sucesso)