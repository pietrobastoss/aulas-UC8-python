# Complete os casos do registro; não marque sucesso sem verificá-los.

from pathlib import Path
import tempfile
import os

from modelos import Pedido, Produto, quantidade, formatar
from repositorio import RepositorioSqlite, validar_preco, validar_nome


def verificar():
    """
    Executa a bateria de verificações automatizadas da Aula 15 via assert.
    Retorna True apenas se todas as asserções e simulações de CRUD passarem com sucesso.
    """
    print("Iniciando verificações da Aula 15 (CRUD de Produtos e Início de Clientes)...")

    # 1. Preservação de casos anteriores (modelos.py)
    assert quantidade(" 5 ") == 5
    assert formatar(1500) == "R$ 15,00"

    pedido = Pedido()
    prod_teste = Produto("P01", "Pizza Margherita", 4000)
    pedido.adicionar(prod_teste, 2)
    assert pedido.total_centavos() == 8000

    # 2. Teste de Persistência SQLite e CRUD em Arquivo Fictício Temporário
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_db = Path(tmpdir) / "teste_crud.db"

        # Instancia e inicializa o repositório SQLite
        repo = RepositorioSqlite(caminho_db)
        assert caminho_db.exists(), "O arquivo de banco de dados SQLite deveria ser criado."

        # C01 & C02: Inserção inicial de produtos
        id_prod1 = repo.adicionar_produto("Copo de Vidro", "5,00")
        id_prod2 = repo.adicionar_produto("Prato Fundo", "12,50")
        assert id_prod1 == 1
        assert id_prod2 == 2

        # C03: Edição de produto por ID (altera nome e preço sem criar nova linha)
        repo.editar_produto(id_prod1, "Copo de Vidro Azul", "6,00")
        produtos = repo.listar_produtos()
        assert len(produtos) == 2, "A edição não deve alterar a quantidade de linhas."
        assert produtos[0]["id"] == id_prod1
        assert produtos[0]["nome"] == "Copo de Vidro Azul"
        assert produtos[0]["preco_centavos"] == 600

        # C04: Tentativa de editar ID inexistente deve lançar ValueError
        try:
            repo.editar_produto(999, "Inexistente", "10,00")
            assert False, "Deveria ter recusado edição de ID inexistente."
        except ValueError:
            pass

        # C05: Exclusão com confirmação cancelada (confirmado=False deve falhar)
        try:
            repo.exclude_produto if hasattr(repo, 'exclude_produto') else repo.excluir_produto(id_prod2, confirmado=False)
            assert False, "Deveria ter exigido confirmação explícita para exclusão."
        except ValueError:
            pass

        # C06: Exclusão confirmada do segundo produto
        repo.excluir_produto(id_prod2, confirmado=True)
        produtos_apos_exclusao = repo.listar_produtos()
        assert len(produtos_apos_exclusao) == 1
        assert produtos_apos_exclusao[0]["id"] == id_prod1

        # C07: Início de Clientes (Adição e Listagem)
        id_cli1 = repo.adicionar_cliente("Maria da Silva")
        assert id_cli1 == 1
        clientes = repo.listar_clientes()
        assert len(clientes) == 1
        assert clientes[0]["nome"] == "Maria da Silva"

        # C08: Reabertura do banco e confirmação de persistência dos dados
        del repo
        repo_reaberto = RepositorioSqlite(caminho_db)
        
        prods_persistidos = repo_reaberto.listar_produtos()
        assert len(prods_persistidos) == 1
        assert prods_persistidos[0]["nome"] == "Copo de Vidro Azul"
        assert prods_persistidos[0]["preco_centavos"] == 600

        clientes_persistidos = repo_reaberto.listar_clientes()
        assert len(clientes_persistidos) == 1
        assert clientes_persistidos[0]["nome"] == "Maria da Silva"

    print("Todas as verificações de CRUD e persistência da Aula 15 passaram com sucesso!")
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
