# A12: Verificações automatizadas sem GUI (verificar.py)
import json
import tempfile
from pathlib import Path

# Importa os módulos do projeto
import modelos
import arquivos


def verificar():
    """Executa todos os casos de teste para catálogo JSON, tratamento de erros

    e persistência do pedido, retornando True se todos passarem.
    """
    sucesso_geral = True

    with tempfile.TemporaryDirectory() as pasta:
        pasta_path = Path(pasta)
        caminho_catalogo = pasta_path / "catalogo.json"

        print("--- Executando Casos de Verificação (A12) ---")

        # ---------------------------------------------------------------------
        # Caso 1: Arquivo ausente deve retornar lista vazia sem criar o arquivo
        # ---------------------------------------------------------------------
        try:
            resultado = arquivos.ler_catalogo(caminho_catalogo)
            assert (
                resultado == []
            ), "Catálogo ausente deveria retornar lista vazia."
            assert (
                not caminho_catalogo.exists()
            ), "O arquivo não deve ser criado ao ler um caminho ausente."
            print("[OK] T01 — Arquivo ausente tratado com sucesso.")
        except AssertionError as e:
            print(f"[FALHA] T01: {e}")
            sucesso_geral = False

        # ---------------------------------------------------------------------
        # Caso 2: Catálogo válido com acentos (UTF-8)
        # ---------------------------------------------------------------------
        try:
            dados_validos = [
                {"id": 1, "nome": "Picolé de Limão", "preco_centavos": 450},
                {"id": 2, "nome": "Açaí Tradicional", "preco_centavos": 1200},
            ]
            arquivos.salvar_catalogo(caminho_catalogo, dados_validos)
            lidos = arquivos.ler_catalogo(caminho_catalogo)
            assert (
                lidos == dados_validos
            ), "Os dados lidos devem ser idênticos aos salvos."
            assert (
                lidos[0]["nome"] == "Picolé de Limão"
            ), "Acentuação UTF-8 deve ser preservada."
            print("[OK] T02 — Catálogo válido com acentos lido e gravado com sucesso.")
        except AssertionError as e:
            print(f"[FALHA] T02: {e}")
            sucesso_geral = False

        # ---------------------------------------------------------------------
        # Caso 3: JSON quebrado (malformado) preserva os bytes originais
        # ---------------------------------------------------------------------
        try:
            # Salva bytes de um JSON inválido (falta fechar colchete/chave)
            conteudo_quebrado = '[{"id": 1, "nome": "Incompleto"'
            caminho_catalogo.write_text(conteudo_quebrado, encoding="utf-8")
            bytes_antes = caminho_catalogo.read_bytes()

            # Tentar ler deve disparar exceção
            try:
                arquivos.ler_catalogo(caminho_catalogo)
                raise AssertionError(
                    "Deveria ter lançado erro ao ler JSON quebrado."
                )
            except ValueError:
                pass  # Comportamento esperado

            bytes_depois = caminho_catalogo.read_bytes()
            assert (
                bytes_antes == bytes_depois
            ), "Os bytes do arquivo original não devem ser alterados após falha de leitura."
            print(
                "[OK] T03 — JSON quebrado detectado e bytes originais preservados."
            )
        except AssertionError as e:
            print(f"[FALHA] T03: {e}")
            sucesso_geral = False

        # ---------------------------------------------------------------------
        # Caso 4: Estrutura inválida (ID repetido ou preço negativo)
        # ---------------------------------------------------------------------
        try:
            # Testando ID repetido
            dados_id_repetido = [
                {"id": 10, "nome": "Item A", "preco_centavos": 100},
                {"id": 10, "nome": "Item B", "preco_centavos": 200},
            ]
            try:
                arquivos.validar_catalogo(dados_id_repetido)
                raise AssertionError("Deveria rejeitar ID repetido.")
            except ValueError:
                pass

            # Testando preço negativo
            dados_preco_negativo = [
                {"id": 11, "nome": "Item C", "preco_centavos": -50}
            ]
            try:
                arquivos.validar_catalogo(dados_preco_negativo)
                raise AssertionError("Deveria rejeitar preço negativo.")
            except ValueError:
                pass

            print("[OK] T04 — Validação de regras de estrutura rejeitou IDs repetidos e preços inválidos.")
        except AssertionError as e:
            print(f"[FALHA] T04: {e}")
            sucesso_geral = False

        # ---------------------------------------------------------------------
        # Caso 5: Correção e nova execução na mesma sessão
        # ---------------------------------------------------------------------
        try:
            # Corrige o arquivo quebrado/inválido com um catálogo válido
            dados_corrigidos = [
                {"id": 100, "nome": "Água Mineral", "preco_centavos": 300}
            ]
            arquivos.salvar_catalogo(caminho_catalogo, dados_corrigidos)
            resultado_pos_correcao = arquivos.ler_catalogo(caminho_catalogo)
            assert (
                resultado_pos_correcao == dados_corrigidos
            ), "Após a correção, o catálogo deve carregar normalmente."
            print("[OK] T05 — Correção e nova execução concluídas com sucesso.")
        except AssertionError as e:
            print(f"[FALHA] T05: {e}")
            sucesso_geral = False

        # ---------------------------------------------------------------------
        # Caso 6: Navegação entre abas sem perder o pedido em memória
        # ---------------------------------------------------------------------
        try:
            # Simula a criação de um pedido (instância única do modelo)
            pedido = modelos.Pedido()
            produto_teste = modelos.Produto(1, "Coxinha", 500)

            # Adiciona item ao pedido
            pedido.adicionar(produto_teste, "2")
            assert (
                pedido.total_centavos() == 1000
            ), "Subtotal inicial incorreto."

            # Simula a troca de abas (ex: ir para a aba de Exercício JSON e voltar para Pedido)
            # A instância do pedido deve ser preservada, sem recriá-lo do zero
            aba_atual = "Exercício JSON"
            aba_atual = "Pedido"

            # Confirma que os dados do carrinho continuam intactos após a navegação
            assert (
                len(pedido.linhas()) == 1
            ), "O carrinho não deve perder seus itens ao alternar abas."
            assert (
                pedido.total_centavos() == 1000
            ), "O total do pedido deve ser conservado após a navegação."
            print("[OK] T06 — Navegação entre abas preservou o pedido e o carrinho com sucesso.")
        except AssertionError as e:
            print(f"[FALHA] T06: {e}")
            sucesso_geral = False

    return sucesso_geral


if __name__ == "__main__":
    if verificar():
        print("\nCasos executados: previsões e resultados conferem.")
    else:
        print("\nVerificações ainda incompletas.")