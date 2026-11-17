# Minha demonstração individual — A19

## Demonstração do fluxo
Problema e requisito escolhido: Registro integrado de vendas com múltiplos itens e rollback
Arquivos/caminho e comando: aulas/Aula 19/ - comando de execução `python main.py` e `verificar.py` para testes de integridade.
Fluxo válido com dados fictícios: Cadastro bem-sucedido de cliente (Maria Silva), produtos(Sorvete Chocolate e Morango) e registro de venda contendo 2 itens com pagamento via PIX gerando ID válido.
Caso de erro ou cancelamento: Tentativa de registrar uma venda contendo um item com código inexistente, provocando a execeção de integridade.
Persistência e relatório: Gravação atômica confirmada no SQLite(tabelas clientes,produtos,vendas e itens) e exportação de comprovante detalhado para formato CSV.
Limite e próximo teste: Validação em aula, próximo teste na Aula 20.

## Pergunta técnica individual
Decisão que consigo explicar com código/evidência: Uso de transações atômicas com tratamento de Rollback no repositório (`repositorio.py`). A evidência no código garante que, caso qualquer item da venda falhe (como uma chave estrangeira inválida), a transação inteira é cancelada, impedindo o registro de vendas parciais no banco de dados.

## Comparação com academia
Entidades e IDs observados: Identificação de entidades de clientes, produtos e vendas na sua candidata, mapeadas de forma similar aos IDs sequenciais inteiros observados na amostra fictícia de academia.
Camadas e armazenamento comprovados pela leitura: Separação clara entre `modelos.py` e  `repositorio.py` e regras de controle/apresentação.
O que não pude afirmar somente pelo README:

## Backup em cópia
Origem e destino novo: Arquivos teste_a19.db (origem existente) e backup_a19.db (destino novo criado de forma segura sem sobrescrever bases pré-existentes).
Consulta de dados conhecidos na cópia: Abertura da cópia por uma conexão independente (sqlite3.connect) e consulta bem-sucedida do cliente cadastrado (Maria Silva) com assert confirmado.
Próxima ação após feedback:
