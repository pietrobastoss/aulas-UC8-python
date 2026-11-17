# Meu registro A19 — Academia e demonstrações individuais

Nome/código individual, turma e data: Pietro Bastos

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Sobre a A18: Permite iniciar a demonstração sem explicações orais extensas por meio de um README.md estruturado e testes automatizados.
- Sobre correções: Devem vir acompanhadas de rastreabilidade de código e evidência de reteste.
- Sobre seleção e exclusão: Utilizam identificadores (id) e restrições relacionais antes da remoção definitiva.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- main.py / Views: Interface Tkinter/ttk (com suporte opcional a CustomTkinter) responsável pela interação visual do usuário.
- controller.py / Models: Camada de controle e regras de negócio para pedidos, produtos e clientes (modelos.py).
- repositorio.py: Camada de persistência em banco de dados SQLite (teste_a19.db), com isolamento transacional (Rollback) e operações atômicas.
- backup_sqlite.py: Utilitário de segurança e cópia por conexão dedicada (origem.backup(destino)).

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Minha demonstração apresenta uma execução e uma explicação próprias.
- Previsão: O script principal roda o fluxo de sorveteria e exibe mensagens de sucesso.
- Observado: Executado com sucesso a partir da pasta de ensaio.
- Correção/reteste ou pendência: Concluído sem pendências.

T02 — Demo inclui fluxo válido, falha/cancelamento e persistência/relatório.
- Previsão: Venda com múltiplos itens grava no banco e gera CSV; item com ID inválido gera rollback.
- Observado: Testes em verificar.py passaram integralmente validando sucesso, rollback e exportação para CSV.
- Correção/reteste ou pendência: Concluído.

T03 — Pergunta técnica tem explicação individual, além da tela pronta.
- Previsão: Explicar o uso de transações atômicas apontando o código de tratamento de erro no repositório.
- Observado: Lógica justificada pela garantia de que falhas parciais não sujam o banco de dados.
- Correção/reteste ou pendência: Concluído.

T04 — Mapa da academia distingue entidade, responsabilidade e armazenamento observado.
- Previsão: Comparar a estrutura de dicionários da amostra de academia com o repositório SQLite da sorveteria.
- Observado: Entidades de clientes/produtos mapeadas por ID de forma idêntica à proposta na leitura.
- Correção/reteste ou pendência: Concluído.

T05 — Backup usa destino novo e não sobrescreve cópia anterior.
- Previsão: Função criar_backup recusa executar se o arquivo de destino já existir (FileExistsError).
- Observado: Exceção disparada e validada com assert no script de teste.
- Correção/reteste ou pendência: Concluído.

T06 — Origem ausente não cria silenciosamente banco vazio.
- Previsão: criar_backup dispara FileNotFoundError se o banco de origem não existir.
- Observado: Validação de existência da origem implementada e testada.
- Correção/reteste ou pendência: Concluído.

T07 — Cópia abre e contém registros conhecidos; integridade conferida.
- Previsão: A cópia gerada por conexão independente (origem.backup(destino)) permite consultar o cliente cadastrado.
- Observado: Conexão independente abriu a cópia e o registro (Maria Silva) foi consultado com sucesso.
- Correção/reteste ou pendência: Concluído.

T08 — Entrega exclui ambientes/caches/dados reais e documenta limites.
- Previsão: Arquivos temporários de teste (.db e .csv) são limpos automaticamente ao final da execução.
- Observado: Rotina de limpeza com tratamento de PermissionError operou perfeitamente no Windows.
- Correção/reteste ou pendência: Concluído.

T09 — Feedback indica evidência por indicador e teste de recuperação.
- Previsão: Os resultados do verificar.py fornecem a evidência objetiva exigida para a A20.
- Observado: Testes 100% verdes no terminal.
- Correção/reteste ou pendência: Concluído.

## Explicação individual
- Uma decisão que consigo justificar: O isolamento da lógica de persistência no repositorio.py e o uso de transações atômicas, garantindo integridade de dados e evitando registros parciais de vendas.
- Uma dificuldade, apoio e próxima tentativa: Dificuldade inicial com travamento de arquivos no Windows (PermissionError: [WinError 32]) resolvida com o fechamento explícito das conexões e tratamento de exceção na limpeza.

## Arquivos
- Versão executada e arquivos baixados: main.py, repositorio.py, modelos.py, backup_sqlite.py, verificar.py.
- Caminho de dados fictícios usado (se houver): teste_a19.db e backup_a19.db na pasta da Aula 19.
- Entrega pelo fluxo combinado conferida por mim: Sim.

## Teoria e transferência
- Consigo explicar uma decisão apontando código e execução: Sim, o uso do mecanismo de Rollback em transações SQLite.
- Consigo distinguir existência da cópia de recuperação conferida: Sim, um arquivo criado não prova integridade até que seja aberto por conexão independente e consultado.
- Consigo identificar origem, destino novo e consulta usada para verificar o backup: Sim, implementado em criar_backup e validado via assert.
- Ligação entre o ensaio e meus arquivos da atividade: O script de teste unificou as regras teóricas de transação e backup com o projeto real da sorveteria.
- Minha previsão antes da alteração guiada e o resultado observado: Previsão de bloqueio por arquivo aberto; resolvido com fechamento de ponteiros do SQLite.

## Continuação em casa
- Arquivos/versão executados:
- Pasta e comando usados: aulas/Aula 19/ — python verificar.py.
- Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: O desenvolvimento seguiu  com versionamento local e testes automatizados de integridade, assegurando que o sistema cumpra os requisitos transacionais e de backup seguro semântico exigidos pela UC8.
- Decisão do meu código sobre demonstração sustentada por evidências, comparação de responsabilidades e backup conferido: Mantida isolada em camadas claras e testada via assert.

## Checklist da interface
- Controles e rótulos que conferi: Campos de cadastro e listagem em tabelas ttk.
- Percurso por Tab/Shift+Tab e acionamento: Navegação padrão validada nas janelas principais.
- Mensagem após erro e possibilidade de corrigir: Mensagens de recusa tratadas e exibidas sem travamento.
- Redimensionamento e comportamento que observei: Janelas adaptáveis com pesos configurados nas colunas.

## Pendências
- O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência.
- Caso para nova tentativa em sala: Validação de relacionamentos avançados na A20.

## Para a A20
- Versão que demonstrei: Candidata consolidada da A18 integrada com rotina de backup da A19.
- Evidência observada e feedback recebido: Sucesso nos testes de transação atômica e backup validado.
- Pendência escolhida para revalidar: Relacionamentos e recuperação avançada entre tabelas associadas.
- Entrada, ação e resultado que espero no reteste: Consulta cruzada de dados integrados com sucesso na Aula 20 