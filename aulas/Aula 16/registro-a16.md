# Meu registro A16 — Controllers e contratos: concluir clientes

Nome/código individual, turma e data: Pietro Bastos

## Retomada sem consulta
Minha hipótese inicial para cada item:


## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- **Fluxo:** 
- **Duração dos dados:** Repositório em memória mantém dados apenas durante a execução da instância volátil; SQLite persiste os dados permanentemente em arquivo físico (`dados_a16.db`).

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Controller executa sem importar Tkinter.
Previsão: O CadastroController processa as chamadas puramente via lógica de negócio e exceções, sem acoplamento visual.
Observado: Executou com sucesso em testes automatizados sem instanciar janelas.
Correção/reteste ou pendência: Nenhum ajuste necessário.

T02 — Mesmo contrato com memória/SQLite inclui, lista e edita por ID.
Previsão: Ambos os repositórios respondem exatamente aos mesmos métodos e dicionários de retorno.
Observado: Inclusão, listagem e edição funcionaram idênticos em memória e SQLite.
Correção/reteste ou pendência: Concluído e verificado via `verificar.py`.

T03 — Memória começa vazia numa nova instância; SQLite reabre com dados.
Previsão: Memória perde estado ao reiniciar; SQLite recupera dados salvos anteriormente no arquivo.
Observado: Comportamento confirmado nos testes.
Correção/reteste ou pendência: Concluído.

T04 — Editar/excluir clientes mantém alvo por ID.
Previsão: As alterações e remoções refletem exatamente sobre o ID selecionado.
Observado: Alvo correto atualizado e excluído com sucesso.
Correção/reteste ou pendência: Concluído.

T05 — Cancelar exclusão de cliente não altera banco nem lista.
Previsão: Interromper a confirmação dispara exceção ou recusa a ação, mantendo os registros intactos.
Observado: Banco e listagem preservados após o cancelamento do usuário.
Correção/reteste ou pendência: Concluído.

T06 — Tipo de cadastro desconhecido é rejeitado.
Previsão: O controller levanta `ValueError` ao receber tipos inválidos.
Observado: Rejeição correta capturada nos testes.
Correção/reteste ou pendência: Concluído.

T07 — Falha do repositório é comunicada e conserva formulário.
Previsão: Exceções de salvamento geram mensagens de erro na tela sem limpar os campos de entrada.
Observado: Campos mantidos após falha simulada, permitindo nova tentativa.
Correção/reteste ou pendência: Concluído.

T08 — Cópia retornada pela memória não permite alterar o armazenamento por fora.
Previsão: O uso de `deepcopy` protege o dicionário interno contra mutações externas.
Observado: O estado interno permaneceu protegido e isolado.
Correção/reteste ou pendência: Concluído.

T09 — Componentes mantêm campos/seleções independentes.
Previsão: As abas de produtos e clientes operam com variáveis e estados separados.
Observado: Navegação e seleções independentes sem conflito de foco.
Correção/reteste ou pendência: Concluído.

## Explicação individual
Uma decisão que consigo justificar:
A decisão de separar a coordenação no `CadastroController` permitiu que a interface gráfica focasse estritamente na captura de eventos e exibição de mensagens, enquanto os testes automatizados (`verificar.py`) puderam validar toda a regra de negócio e persistência sem precisar iniciar o ambiente gráfico do Tkinter.

Uma dificuldade, apoio e próxima tentativa:
Dificuldade inicial com a formatação e captura de valores vazios nos campos da interface. O apoio veio da revisão dos contratos de validação e da estrutura de tratamento de exceções nos callbacks de salvamento.

## Arquivos
Versão executada e arquivos baixados: 
modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, repositorio.py, controller.py, memoria.py, verificar.py, main.py, registro-a16.md
Caminho de dados fictícios usado (se houver): dados_a16.db / arquivos temporários em disco.
Entrega pelo fluxo combinado conferida porខ្ញុំ (sim): Conferido.

## Teoria e transferência
Consigo seguir uma chamada da interface ao controller e ao repositório.
Minha explicação: O clique no botão da interface lê os valores crus dos campos, os repassa como argumentos simples para os métodos do controller, que valida e delega a operação de persistência ao repositório correspondente.

Consigo descrever o contrato e o que fica igual nas duas implementações.
Minha explicação: O contrato define os nomes exatos dos métodos, tipos de argumentos e formato dos retornos (dicionários e listas). Tanto o `RepositorioMemoria` quanto o `RepositorioSqlite` cumprem esse mesmo contrato.

Consigo distinguir a duração dos dados em memória e SQLite.
Minha explicação: Dados em memória existem apenas durante o tempo de vida da instância volátil da aplicação, enquanto o SQLite grava os dados permanentemente em um arquivo físico no disco.

Ligação entre o ensaio e meus arquivos da atividade: O ensaio demonstrou como um coordenador delega chamadas sem widgets, conceito aplicado integralmente no `CadastroController`.
Minha previsão antes da alteração guiada e o resultado observado: Previsão de que a separação isolaria erros visuais de erros de banco, confirmada durante os testes automatizados.

## Continuação em casa
Arquivos/versão executados: 
Pasta e comando usados: `python verificar.py` e `python main.py` na pasta `Aula 16`.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
A adoção de um controller centralizado evitou a duplicação de regras de negócio dentro dos callbacks da interface gráfica. O contrato de repositório garantiu que a troca entre persistência volátil (memória) e permanente (SQLite) ocorresse de forma transparente para o chamador. Além disso, o tratamento adequado de exceções assegurou que falhas de armazenamento não destruíssem os dados digitados pelo usuário, preservando a usabilidade da aplicação.

Decisão do meu código sobre controller, contrato de repositório, componentes e conclusão do CRUD de clientes: Implementação padronizada do CRUD completo de clientes e produtos, garantindo validação de IDs, nomes e confirmação obrigatória de exclusão.
Minha explicação / anexo: Código integrado e testado sem pendências.

## Checklist da interface
Controles e rótulos que conferi: Abas de Produtos e Clientes, formulários, botões de ação e tabelas Treeview.
Percurso por Tab/Shift+Tab e acionamento: Navegação fluida entre os campos de entrada e botões de controle.
Mensagem após erro e possibilidade de corrigir: Mensagens claras exibidas via `messagebox` e rótulo local, mantendo os campos preenchidos.
Redimensionamento e comportamento que observei: Janela responsiva com grade configurada (`weight=1`).

## Pendências
O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência; todos os testes automatizados e fluxos de interface foram executados e aprovados.
Caso para nova tentativa em sala: 