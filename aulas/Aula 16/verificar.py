# Complete os casos do registro; não marque sucesso sem verificá-los.

import os
import tempfile
from memoria import RepositorioMemoria
from repositorio import RepositorioSqlite
from controller import CadastroController

def verificar():
    print("Iniciando verificações sem GUI para a Aula 16...")
    
    # Arquivo temporário para testar o SQLite
    fd, caminho_db = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    
    try:
        # Testando com ambos os repositórios (Contrato idêntico)
        repositorios = [
            ("Memória", RepositorioMemoria()),
            ("SQLite", RepositorioSqlite(caminho_db))
        ]
        
        for nome_repo, repo in repositorios:
            print(f"\n--- Testando com Repositório: {nome_repo} ---")
            controller = CadastroController(repo)
            
            # 1. Testar Listagem Inicial Vazia
            assert controller.listar("produto") == [], f"[{nome_repo}] Produtos iniciais devem estar vazios."
            assert controller.listar("cliente") == [], f"[{nome_repo}] Clientes iniciais devem estar vazios."
            
            # 2. Testar Inclusão de Produto e Cliente
            prod_criado = controller.salvar("produto", "Café Expresso", "5,50")
            assert prod_criado["id"] == 1
            assert prod_criado["nome"] == "Café Expresso"
            assert prod_criado["preco_centavos"] == 550
            
            cli_criado = controller.salvar("cliente", "Maria Silva")
            assert cli_criado["id"] == 1
            assert cli_criado["nome"] == "Maria Silva"
            
            # 3. Testar Listagem Após Inclusão
            produtos = controller.listar("produto")
            assert len(produtos) == 1
            assert produtos[0]["nome"] == "Café Expresso"
            
            clientes = controller.listar("cliente")
            assert len(clientes) == 1
            assert clientes[0]["nome"] == "Maria Silva"
            
            # 4. Testar Edição por ID
            prod_editado = controller.salvar("produto", "Café Premium", "6,00", codigo=prod_criado["id"])
            assert prod_editado["id"] == prod_criado["id"]
            assert prod_editado["nome"] == "Café Premium"
            assert prod_editado["preco_centavos"] == 600
            
            cli_editado = controller.salvar("cliente", "Maria da Silva Santos", codigo=cli_criado["id"])
            assert cli_editado["id"] == cli_criado["id"]
            assert cli_editado["nome"] == "Maria da Silva Santos"
            
            # 5. Testar Exclusão com e sem Confirmação (Cancelamento)
            # Cancelamento (confirmado=False deve gerar ValueError)
            try:
                controller.excluir("produto", prod_criado["id"], confirmado=False)
                raise AssertionError("Deveria ter lançado ValueError ao não confirmar exclusão.")
            except ValueError:
                pass # Comportamento esperado
            
            # Garantir que o produto ainda existe após cancelamento da exclusão
            assert len(controller.listar("produto")) == 1
            
            # Exclusão efetiva (confirmada=True)
            controller.excluir("produto", prod_criado["id"], confirmado=True)
            assert controller.listar("produto") == [], f"[{nome_repo}] Produto deveria ter sido excluído."
            
            # 6. Testar Rejeição de Tipo Desconhecido
            try:
                controller.listar("fornecedor")
                raise AssertionError("Deveria rejeitar tipo desconhecido.")
            except ValueError:
                pass # Comportamento esperado

        print("\nTodas as verificações passaram com sucesso!")
        return True

    except Exception as e:
        print(f"\n[ERRO NA VERIFICAÇÃO]: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Limpa o arquivo de banco temporário do SQLite
        if os.path.exists(caminho_db):
            os.remove(caminho_db)

if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
