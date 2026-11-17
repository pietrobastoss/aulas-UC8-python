# Meu registro A18 — Regressão, correções e README reproduzível

Nome/código individual, turma e data: Pietro Bastos

## Retomada sem consulta
Minha hipótese inicial para cada item:


## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- **Módulos:** `modelos.py` (regras e entidades), `pagamento.py` (cálculos e conversões), `repositorio.py` (persistência SQLite), `arquivos.py` (JSON), `relatorios.py` (exportação CSV), `perfis.py` (sessão) e `verificar.py` (suíte de testes automatizados com `assert`).
- **Dependências:** `modelos` e `pagamento` são base; `repositorio` persiste dados transacionais; `verificar.py` orquestra a validação lógica.
- **Duração dos dados:** Dados de catálogo e vendas persistem no SQLite de ensaio; estados de montagem residem na memória da aplicação até a confirmação.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Valores conhecidos, erro após válido e cancelamento repetidos.
Previsão: O sistema aceita valores válidos, rejeita entradas inválidas com `ValueError` e limpa/reinicia o pedido ao cancelar.
Observado: Comportamento validado via testes e testes interativos.
Correção/reteste ou pendência: Nenhum erro remanescente.

T02 — ID estável após reorganizar listagem.
Previsão: Os IDs primários dos produtos e clientes permanecem inalterados independentemente da ordem de exibição.
Observado: Chaves primárias mantidas com integridade relacional.
Correção/reteste ou pendência: Sucesso na listagem ordenada.

T03 — Persistência reaberta no mesmo caminho.
Previsão: Ao fechar e reabrir a conexão com o arquivo SQLite de ensaio, os registros anteriores continuam acessíveis.
Observado: Dados lidos corretamente após reconexão.
Correção/reteste ou pendência: Persistência validada.

T04 — Falha transacional sem venda parcial.
Previsão: Inserir um item inválido (ex.: ID inexistente) aciona o rollback, impedindo gravação parcial de vendas.
Observado: Nenhuma venda parcial foi gravada no banco de dados.
Correção/reteste ou pendência: Transação atômica confirmada por `assert`.

T05 — Exportação CSV coerente com o comprovante.
Previsão: O arquivo gerado contém exatamente os campos e itens especificados no comprovante confirmado.
Observado: Arquivo CSV gerado e validado estruturalmente.
Correção/reteste ou pendência: Sem divergências.

T06 — Teste propositalmente errado falha; previsão restaurada passa.
Previsão: Alterar a expectativa para um valor incorreto dispara `AssertionError`; ao restaurar o valor real, passa sem erros.
Observado: Falha detectada corretamente e reteste bem-sucedido.
Correção/reteste ou pendência: Comportamento esperado dos testes com `assert`.

T07 — Execução pelo README em outra pasta.
Previsão: Outro usuário consegue clonar/copiar a pasta e executar `python verificar.py` seguindo estritamente as instruções do README.
Observado: Execução limpa e reprodutível.
Correção/reteste ou pendência: Documentação validada.

T08 — Teclado, foco e mensagens inspecionados.
Previsão: Os campos aceitam navegação via Tab e exibem mensagens claras em caso de falha de validação.
Observado: Foco funcional e atalhos operando conforme esperado.
Correção/reteste ou pendência: Sem pendências visuais críticas.

T09 — Pendências identificadas sem inventar aprovação.
Previsão: Funcionalidades incompletas são explicitamente documentadas sem fingir que estão prontas.
Observado: Limites claramente descritos no README.
Correção/reteste ou pendência: Transparência mantida.

## Explicação individual
Uma decisão que consigo justificar: O uso da biblioteca `Decimal` com arredondamento `ROUND_HALF_UP` nas conversões monetárias para eliminar erros de arredondamento inerentes ao ponto flutuante em Python.
Uma dificuldade, apoio e próxima tentativa: Garantir o isolamento completo do banco de dados de ensaio em testes automatizados, superado utilizando arquivos temporários/fixtures dedicadas via `pathlib`.

## Arquivos
Versão executada e arquivos baixados: `modelos.py`, `pagamento.py`, `repositorio.py`, `relatorios.py`, `verificar.py`, `README-A18.md`.
Caminho de dados fictícios usado (se houver): `dados/sorveteria_ensaio.db`
Entrega pelo fluxo combinado conferida por mim: Sim.

## Teoria e transferência
Consigo explicar a origem independente da expectativa de um teste.
Minha explicação: A expectativa deve ser calculada ou conhecida antes de chamar a função, sem depender de reexecutar a lógica interna sob teste.
Consigo escolher um caso vizinho para conferir uma correção.
Minha explicação: Selecionando um cenário adjacente que utilize a mesma função modificada (como uma quantidade alterada ou tipo de pagamento diferente) para garantir que o comportamento geral não foi corrompido.
Consigo orientar outra pessoa a executar pelo README com dados de ensaio.
Minha explicação: Indicando os comandos exatos de terminal (`python verificar.py`) e o caminho dos arquivos de ensaio isolados.
Ligação entre o ensaio e meus arquivos da atividade: Os testes em `verificar.py` cobrem diretamente as regras de `modelos.py` e `repositorio.py`.
Minha previsão antes da alteração guiada e o resultado observado: Previsão de falha controlada ao alterar assertivas e sucesso na execução após correção.

## Continuação em casa
Arquivos/versão executados: 
Pasta e comando usados: 
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: A estruturação de testes de regressão com `assert` e a documentação via `README` garantem a auditabilidade e reprodutibilidade do software, permitindo que qualquer alteração futura seja validada de forma automatizada sem riscos de regressões ocultas.
Decisão do meu código sobre regressão, expectativa independente, isolamento de dados e README reproduzível: Aplicação robusta com testes automatizados isolados e instruções claras para replicação em ambiente limpo.
Minha explicação / anexo: Documentado no repositório local.

## Checklist da interface
Controles e rótulos que conferi: Campos de entrada de quantidade, listagem de itens e botões de finalização.
Percurso por Tab/Shift+Tab e acionamento: Navegação fluida entre os elementos de entrada.
Mensagem após erro e possibilidade de corrigir: Mensagens de validação exibidas sem travamento da aplicação.
Redimensionamento e comportamento que observei: Janela responsiva com layout estável em CustomTkinter.

## Pendências
O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência impeditiva registrada.
Caso para nova tentativa em sala: 

## Para a A19
Pasta ou revisão da candidata: Pasta `Aula 18` contendo todos os módulos validados.
Instrução que o colega conseguiu executar: Rodar `python verificar.py` e iniciar a interface com banco de ensaio isolado.
Caso que vou demonstrar e evidência disponível: Simulação de venda completa, validação de transação atômica (rollback) e exportação de relatório CSV.
Limite ou próximo teste: Ajustes finais.
