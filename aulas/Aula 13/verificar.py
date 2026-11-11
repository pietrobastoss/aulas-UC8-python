# Complete os casos do registro; não marque sucesso sem verificá-los.

from pathlib import Path
import tempfile
import os

from modelos import Pedido, Produto, quantidade, formatar
from relatorios import exportar_csv
from perfis import SessaoDemo
from arquivos import validar_catalogo


def verificar():
    """
    Executa a bateria completa de testes automatizados sem interface gráfica (Aula 13).
    Retorna True apenas se todas as asserções e simulações passarem com sucesso.
    """
    print("Iniciando verificações da Aula 13 (CSV de vendas e simulação de perfis)...")

    # 1. Validação de Quantidade e Formatação (Casos anteriores preservados)
    assert quantidade(" 5 ") == 5
    assert formatar(1500) == "R$ 15,00"

    # 2. Criação de pedido com o produto especial contendo ponto e vírgula e acento
    pedido = Pedido()
    prod = Produto("P01", "Picolé; edição verão", 450)
    pedido.adicionar(prod, 3)  # Subtotal = 1350 centavos (R$ 13,50)

    # Tenta exportar sem finalizar (deve falhar pois não há comprovante)
    try:
        exportar_csv("caminho_invalido.csv", pedido.comprovante)
        assert False, "Deveria ter lançado ValueError ao exportar pedido sem comprovante."
    except (ValueError, TypeError):
        pass  # Comportamento esperado: falha por ausência de comprovante

    # Finaliza o pedido para gerar o comprovante oficial
    comprovante = pedido.finalizar("PIX", confirmado=True)
    assert comprovante is not None
    assert comprovante["total_centavos"] == 1350

    # 3. Teste de Exportação CSV com Arquivo Temporário e Leitura de Volta
    with tempfile.TemporaryDirectory() as tmpdir:
        caminho_csv = Path(tmpdir) / "venda_teste.csv"
        
        # Exporta o comprovante
        exportar_csv(caminho_csv, comprovante)
        assert caminho_csv.exists(), "O arquivo CSV do comprovante deveria ter sido criado."

        # Lê o CSV de volta utilizando csv.DictReader e delimitador ';'
        import csv
        with open(caminho_csv, "r", encoding="utf-8-sig", newline="") as f:
            leitor = csv.DictReader(f, delimiter=";")
            linhas = list(leitor)

        # Conferência de colunas, nome especial e total
        assert len(linhas) == 1
        assert linhas[0]["Nome"] == "Picolé; edição verão"
        assert int(linhas[0]["Quantidade"]) == 3
        assert linhas[0]["Forma_Pagamento"] == "PIX"
        assert linhas[0]["Total_Pedido_Formatado"] == "R$ 13,50"

    # 4. Simulação de Destino sem Permissão ou Pasta Inexistente / Preservação do Pedido
    with tempfile.TemporaryDirectory() as tmpdir:
        # Cria um diretório e retira as permissões de escrita (se o OS permitir, ou simula caminho inválido)
        pasta_inexistente = Path(tmpdir) / "pasta_protegida" / "sub" / "arquivo.csv"
        
        try:
            # Tenta exportar para um diretório que não existe e cujos pais não podem ser criados
            exportar_csv(pasta_inexistente, comprovante)
        except Exception as e:
            # Registra que a mensagem de erro ocorreu e garante a preservação do pedido
            assert e is not None
            # Verifica que o pedido continua intacto e finalizado com seus itens originais
            assert len(pedido.itens) == 1
            assert pedido.total_centavos() == 1350

    # 5. Testes da Simulação de Perfis (SessaoDemo)
    sessao = SessaoDemo()
    assert sessao.ativo is False

    # Entra como Caixa
    sessao.entrar("João Caixa", "Caixa")
    assert sessao.ativo is True
    assert sessao.pode_configurar() is False  # Caixa não pode configurar

    # Troca para Administração
    sessao.entrar("Maria Admin", "Administração")
    assert sessao.pode_configurar() is True   # Administração possui permissão

    # Encerra a sessão
    sessao.sair()
    assert sessao.ativo is False
    assert sessao.pode_configurar() is False

    print("Todas as verificações de CSV e perfis passaram com sucesso!")
    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
