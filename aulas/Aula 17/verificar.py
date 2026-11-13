# Complete os casos do registro; não marque sucesso sem verificá-los.

from pathlib import Path
import os
from repositorio import RepositorioSqlite
from modelos import Pedido, Produto
from relatorios import exportar_csv

def verificar():
    caminho_db = Path("teste_a17.db")
    if caminho_db.exists():
        caminho_db.unlink()

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

        # Confirma que a venda e os itens foram gravados corretamente
        vendas_listadas = repo.listar_vendas()
        assert len(vendas_listadas) == 1, "Deveria existir exatamente uma venda registrada."
        assert len(vendas_listadas[0]["itens"]) == 2, "A venda deve conter exatamente 2 itens."

        # 3. Testa FALHA NA TRANSAÇÃO (Rollback / Sem venda parcial)
        # Tentamos registrar uma venda onde o segundo item possui um produto inexistente (ID 9999)
        itens_falha = [
            {"codigo": p1_id, "nome": "Sorvete Chocolate", "preco_unitario": 500, "quantidade": 1, "subtotal": 500},
            {"codigo": 9999, "nome": "Produto Inexistente", "preco_unitario": 1000, "quantidade": 1, "subtotal": 1000}
        ]
        
        total_vendas_antes = len(repo.listar_vendas())
        try:
            repo.registrar_venda(cli_id, itens_falha, "Dinheiro")
            raise AssertionError("Deveria ter falhado ao registrar item com ID inexistente.")
        except Exception:
            # Esperado devido à violação de chave estrangeira ou integridade
            pass

        total_vendas_depois = len(repo.listar_vendas())
        assert total_vendas_antes == total_vendas_depois, "O rollback deve impedir a gravação de venda parcial em caso de falha."

        # 4. Testa modelo de Pedido e finalização com comprovante para CSV
        pedido = Pedido()
        p_obj = Produto(p1_id, "Sorvete Chocolate", 500)
        pedido.adicionar(p_obj, "2")
        
        comprovante = pedido.finalizar("PIX", confirmado=True)
        assert comprovante["total_centavos"] == 870, "O total com desconto PIX (0.87) de R$ 10,00 deve ser 870 centavos."

        # Testa exportação de relatório CSV
        caminho_csv = Path("teste_comprovante.csv")
        if caminho_csv.exists():
            caminho_csv.unlink()
            
        exportar_csv(caminho_csv, comprovante)
        assert caminho_csv.exists(), "O arquivo CSV do comprovante deve ser gerado com sucesso."
        
        # Limpeza dos arquivos temporários de teste
        if caminho_csv.exists():
            caminho_csv.unlink()
        if caminho_db.exists():
            caminho_db.unlink()

        return True

    except Exception as e:
        print(f"Erro durante a verificação: {e}")
        if caminho_db.exists():
            caminho_db.unlink()
        return False


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
