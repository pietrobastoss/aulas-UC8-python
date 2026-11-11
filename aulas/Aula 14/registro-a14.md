# Meu registro A14 — SQLite: produtos que permanecem após reabrir

Nome/código individual, turma e data: Pietro Bastos 

## Retomada sem consulta
Minha hipótese inicial para cada item:


## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- main.py (Interface gráfica / Tkinter) -> RepositorioSqlite (repositorio.py) -> Banco SQLite em arquivo local (`dados_pizzaria.db`).
- Produtos persistem no banco de dados SQLite entre execuções; os itens do carrinho e montagem de pedidos continuam residindo temporariamente em memória.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Tabela criada sem apagar linhas existentes.
Previsão: O uso de `CREATE TABLE IF NOT EXISTS` criará a estrutura apenas se ela não existir, preservando os registros anteriores.
Observado: Tabela criada com sucesso e linhas pré-existentes mantidas intactas após novas instanciações de `RepositorioSqlite`.
Correção/reteste ou pendência: Conforme previsto, nenhum dado foi perdido.

T02 — Preço 7,50 gravado como 750 inteiro.
Previsão: A função `validar_preco` converterá o texto monetário `"7,50"` via `preco_para_centavos` para o inteiro `750`.
Observado: O valor armazenado na coluna `preco_centavos` foi exatamente `750`.
Correção/reteste ou pendência: Comportamento validado com sucesso pelo `verificar.py`.

T03 — Nome com apóstrofo tratado como parâmetro literal.
Previsão: O uso de placeholders `?` no método `execute` impedirá que o apóstrofo em `"Picolé d'água"` corrompa o SQL.
Observado: O registro foi inserido e consultado sem erros de sintaxe.
Correção/reteste ou pendência: Nenhuma falha observada; parâmetros separados garantiram segurança total.

T04 — Nome vazio/preço inválido não insere registro.
Previsão: Validações internas (`validar_nome` e `validar_preco`) lançarão `ValueError` e abortarão a transação.
Observado: Entradas vazias ou negativas foram rejeitadas corretamente sem alterar o estado do banco.
Correção/reteste ou pendência: Campos mantidos na interface para correção pela pessoa usuária.

T05 — IDs positivos únicos, independentes da posição visual.
Previsão: O uso de `INTEGER PRIMARY KEY AUTOINCREMENT` garantirá IDs inteiros crescentes e únicos por linha.
Observado: Cada produto inserido recebeu um ID exclusivo e sequencial, inalterado por ordenações visuais.
Correção/reteste ou pendência: Comprovado na listagem da Treeview e consultas SQL.

T06 — Reabrir o mesmo arquivo conserva produtos.
Previsão: Ao instanciar `RepositorioSqlite` apontando para o mesmo caminho de arquivo `.db`, os produtos cadastrados continuarão disponíveis.
Observado: A listagem recuperou todos os itens inseridos antes do fechamento da conexão.
Correção/reteste ou pendência: Persistência física comprovada com sucesso.

T07 — Falha de conexão/gravação não deve aparecer como sucesso.
Previsão: A interface só exibirá mensagem de sucesso e limpará os campos após o retorno sem exceções da persistência.
Observado: Mensagens de erro de validação impediram o reset do formulário, mantendo os dados digitados visíveis.
Correção/reteste ou pendência: Comportamento defensivo validado na aba Produtos.

T08 — Conexões fechadas; importar não cria banco.
Previsão: O simples carregamento (import) dos módulos Python não deve disparar abertura de arquivos ou criação de tabelas.
Observado: Módulos importados de forma limpa, sem efeitos colaterais indesejados.
Correção/reteste ou pendência: Conexões gerenciadas via `closing` e blocos `with con`.

T09 — Pedido em memória continua separado dos produtos persistidos.
Previsão: A persistência em SQLite afeta a tabela de produtos cadastrados; o carrinho de compras atual permanece isolado em memória.
Observado: A arquitetura manteve o catálogo no banco e o pedido ativo na classe `Pedido`.
Correção/reteste ou pendência: Separação de responsabilidades respeitada.

## Explicação individual
Uma decisão que consigo justificar:
A adoção de consultas parametrizadas (`?`) em todas as operações de escrita no `repositorio.py`, pois elimina completamente vulnerabilidades de injeção de SQL e soluciona de forma nativa o tratamento de caracteres especiais (como apóstrofos em nomes de produtos).

Uma dificuldade, apoio e próxima tentativa:
A principal atenção foi garantir que o caminho do banco de dados fosse resolvido de forma absoluta (`Path.resolve()`) para evitar a criação duplicada de arquivos `.db` ao executar scripts a partir de diretórios diferentes no terminal. Na próxima etapa (A15), o foco será expandir o CRUD completo para clientes e produtos.

## Arquivos
Versão executada e arquivos baixados: 
Caminho de dados fictícios usado (se houver): 
Entrega pelo fluxo combinado conferida por mim: 

## Teoria e transferência
Consigo explicar persistência e a diferença para memória.
Minha explicação: Persistência é a capacidade de salvar dados permanentemente em suportes não voláteis (como arquivos em disco ou bancos SQLite), de forma que sobrevivam ao encerramento da aplicação, diferenciando-se da memória RAM, que é volátil e apagada ao fechar o programa.

Consigo localizar comando, parâmetros e confirmação da gravação.
Minha explicação: O comando SQL fica isolado na string de instrução (ex: `INSERT INTO ... VALUES (?, ?)`), os valores são passados de forma segura na tupla de parâmetros subsequente, e a confirmação transacional é efetivada por meio do gerenciamento de contexto do banco (`with con`).

Consigo indicar quando usar JSON, CSV ou SQLite nas atividades do curso.
Minha explicação: Usamos JSON para estruturação hierárquica de catálogos e configurações; CSV para intercâmbio tabular de relatórios e comprovantes; e SQLite para bases relacionais que exigem consultas rápidas, integridade de chaves e persistência escalável de registros.

Ligação entre o ensaio e meus arquivos da atividade: O ensaio em memória (`:memory:`) serviu para validar a sintaxe dos comandos SQL, enquanto a atividade prática expandiu o conceito para arquivos físicos em disco, testando reabertura e robustez contra entradas inválidas.

Minha previsão antes da alteração guiada e o resultado observado: Previa que nomes com apóstrofo quebrariam o SQL sem parâmetros explícitos; o teste confirmou que o uso de `?` preservou o dado exatamente como digitado.

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados: 
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
A decisão de centralizar a persistência de produtos na classe `RepositorioSqlite` garante que a interface gráfica (`main.py`) e os testes automatizados (`verificar.py`) compartilhem exatamente a mesma regra de acesso ao banco. O uso de parâmetros separados protege contra erros de sintaxe em nomes como "Picolé d'água", enquanto a transação gerenciada por contexto assegura que operações inválidas sejam descartadas sem corromper o arquivo de dados.

## Checklist da interface
Controles e rótulos que conferi: Campos de nome e preço, rótulos descritivos da aba, tabela `Treeview` com colunas de ID, Nome e Preço em centavos.
Percurso por Tab/Shift+Tab e acionamento: Navegação fluida entre os campos de entrada, botão Salvar acionável por Enter ou barra de espaço.
Mensagem após erro e possibilidade de corrigir: Mensagens de erro exibidas em destaque vermelho, mantendo os dados no formulário para imediata correção.
Redimensionamento e comportamento que observei: Layout fluido adaptando-se corretamente ao redimensionamento da janela graças ao uso de `weight` nas linhas e colunas.

## Pendências
O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência; todos os casos do roteiro e testes de repositório foram executados com sucesso no ambiente local.
Caso para nova tentativa em sala: