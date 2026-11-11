# Complete os casos do registro; não marque sucesso sem verificá-los.

from pathlib import Path
import tempfile
import os

from modelos import Pedido, Produto, quantidade, formatar
from repositorio import RepositorioSqlite, validar_preco, validar_nome


def verificar():
    """
    Executa a bateria de verificações automatizadas da Aula 14 via assert.
    Retorna True apenas se todas as asserções e simulações passarem com sucesso.
    """
    print("Iniciando verificações da Aula 14 (SQLite e Persistência de Produtos)...")

    # 1. Preservação de casos anteriores (modelos.py)
    assert quantidade(" 3 ") == 3
    assert formatar(750) == "R$ 7,50"

    pedido = Pedido()
    prod_teste = Produto("P01", "Pizza Margherita", 4000)
    pedido.adicionar(prod_teste, 2)
    assert pedido.total_centavos() == 8000

    # 2. Teste de Persistência SQLite em Arquivo Fictício Temporário
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_db = Path(tmpdir) / "teste_produtos.db"

        # Instancia e inicializa o repositório SQLite
        repo = RepositorioSqlite(caminho_db)
        assert caminho_db.exists(), "O arquivo de banco de dados SQLite deveria ser criado."

        # T01 & T02: Inserção de preço decimal convertido para centavos inteiros (7,50 -> 750)
        id_prod1 = repo.adicionar_produto("Picolé de Morango", "7,50")
        assert id_prod1 is not None and id_prod1 > 0

        # T03: Tratamento de nome com apóstrofo via consulta SQL parametrizada
        nome_apostrofo = "Picolé d'água"
        id_prod2 = repo.adicionar_produto(nome_apostrofo, "4,50")
        assert id_prod2 > id_prod1

        # Listagem inicial e validação dos dados gravados
        produtos = repo.listar_produtos()
        assert len(produtos) == 2
        assert produtos[1]["nome"] == "Picolé d'água"
        assert produtos[1]["preco_centavos"] == 450

        # T04: Teste de entradas inválidas (deve lançar ValueError sem alterar o banco)
        try:
            repo.adicionar_produto("", "10,00")
            assert False, "Deveria ter recusado nome vazio."
        except ValueError:
            pass

        try:
            repo.adicionar_produto("Produto Inválido", "-5,00")
            assert False, "Deveria ter recusado preço negativo."
        except ValueError:
            pass

        try:
            repo.adicionar_produto("Produto Limite Excedido", "150000,00")
            assert False, "Deveria ter recusado preço acima do limite didático."
        except ValueError:
            pass

        # Garante que o banco continua contendo apenas os 2 registros válidos
        produtos_apos_erros = repo.listar_produtos()
        assert len(produtos_apos_erros) == 2

        # T06: Fechamento da conexão e reabertura do MESMO caminho para comprovar persistência
        del repo
        repo_reaberto = RepositorioSqlite(caminho_db)
        produtos_persistidos = repo_reaberto.listar_produtos()

        assert len(produtos_persistidos) == 2
        assert produtos_persistidos[0]["nome"] == "Picolé de Morango"
        assert produtos_persistidos[0]["preco_centavos"] == 750
        assert produtos_persistidos[1]["nome"] == "Picolé d'água"
        assert produtos_persistidos[1]["preco_centavos"] == 450

    print("Todas as verificações de SQLite e persistência passaram com sucesso!")
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
