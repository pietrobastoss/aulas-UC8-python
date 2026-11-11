# Meu registro A15 — CRUD: editar produtos e iniciar clientes

Nome/código individual, turma e data: Pietro Bastos

## Retomada sem consulta
Minha hipótese inicial para cada item:

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- main.py (Interface Tkinter com Notebook e Treeview) -> RepositorioSqlite (repositorio.py) -> Banco SQLite em arquivo local (`dados_pizzaria.db`).
- Produtos possuem CRUD completo (criar, consultar, atualizar por ID e excluir com confirmação); clientes iniciam com inclusão e listagem; itens do pedido continuam efêmeros em memória.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Editar por ID preserva a identidade e não duplica linha.
Previsão: O comando `UPDATE ... WHERE id = ?` alterará os atributos do registro sem alterar sua chave primária ou criar novas linhas.
Observado: Linha atualizada com sucesso mantendo o mesmo ID.
Correção/reteste ou pendência: Comportamento validado sem duplicatas.

T02 — Editar após mover a linha altera o produto certo.
Previsão: Como a atualização utiliza o ID armazenado no estado da seleção e não a posição visual na Treeview, o produto correto será alterado.
Observado: Mesmo após reordenar a listagem, a edição modificou exatamente o ID pretendido.
Correção/reteste ou pendência: Nenhuma divergência observada.

T03 — Preço/nome inválido preserva valor persistido.
Previsão: Exceções de validação (`ValueError`) abortarão a transação e manterão os campos preenchidos na interface para correção.
Observado: Os dados anteriores no banco e os valores digitados na tela foram preservados intactos.
Correção/reteste ou pendência: Validação defensiva funcionando conforme esperado.

T04 — ID inexistente não recebe mensagem de sucesso.
Previsão: O uso de verificação do `rowcount` identificará que nenhuma linha foi afetada, impedindo a exibição de mensagem de sucesso.
Observado: Exceção disparada corretamente ao tentar editar ID inexistente.
Correção/reteste ou pendência: Mensagem clara exibida na interface.

T05 — Excluir sem seleção pede uma escolha.
Previsão: A interface emitirá um aviso se o usuário acionar a exclusão sem nenhum item selecionado na Treeview.
Observado: Alerta exibido solicitando a seleção de um registro.
Correção/reteste ou pendência: Comportamento preventivo validado.

T06 — Cancelar exclusão preserva dados e tela.
Previsão: Responder "Não" na caixa de diálogo de confirmação abortará a exclusão, mantendo o registro no banco e na listagem.
Observado: Registro preservado exatamente como estava.
Correção/reteste ou pendência: Testado e aprovado.

T07 — Confirmar exclui só o ID escolhido e atualiza lista.
Previsão: Responder "Sim" executará o `DELETE` pelo ID, removendo a linha do banco e redesenhando a Treeview.
Observado: Linha removida com sucesso e listagem atualizada.
Correção/reteste ou pendência: Nenhuma pendência.

T08 — Excluir último registro deixa lista vazia utilizável.
Previsão: A remoção do último item deixará a tabela vazia sem quebrar a aplicação, permitindo novas inclusões imediatas.
Observado: Tabela esvaziada e pronta para novos cadastros.
Correção/reteste ou pendência: Comportamento estável verificado.

T09 — Clientes fictícios incluídos/listados e persistidos.
Previsão: A nova tabela de clientes no SQLite armazenará e listará os nomes cadastrados com sucesso.
Observado: Clientes inseridos e listados corretamente na aba dedicada.
Correção/reteste ou pendência: Módulo de clientes integrado.

T10 — Reabrir conserva edição/exclusão efetivamente confirmadas.
Previsão: Ao reabrir a aplicação, o banco refletirá o estado final pós-edições e exclusões.
Observado: Dados persistidos corretamente após reiniciar o script.
Correção/reteste ou pendência: Persistência física validada.

## Explicação individual
Uma decisão que consigo justificar:
A utilização de `rowcount` nas operações de atualização (`editar_produto`) e exclusão (`excluir_produto`) no `repositorio.py`. Isso garante que o sistema só confirme o sucesso de uma alteração se a linha realmente existir no banco, evitando mensagens falsas de sucesso em IDs inexistentes.

Uma dificuldade, apoio e próxima tentativa:
Garantir que o botão "Novo" limpasse corretamente a variável de controle do ID selecionado para que o próximo clique em Salvar realizasse uma inclusão (`INSERT`) em vez de uma edição (`UPDATE`). O ajuste foi simples e validado via testes.

## Arquivos
Versão executada e arquivos baixados: 
Caminho de dados fictícios usado (se houver): 
Entrega pelo fluxo combinado conferida por mim: 

## Teoria e transferência
Consigo distinguir inclusão, edição e exclusão.
Minha explicação: Inclusão adiciona um novo registro gerando um ID inédito; edição modifica os atributos de um registro existente mantendo sua identidade por ID; exclusão remove permanentemente o registro com base no seu identificador unívoco.

Consigo justificar a preservação do ID ao editar.
Minha explicação: O ID representa a identidade imutável da entidade no banco de dados relacional. Alterá-lo quebraria relações com pedidos e histórico, enquanto atualizar apenas os campos descritivos mantém a integridade dos dados.

Consigo prever os dados após Cancelar e o comportamento com lista vazia.
Minha explicação: Cancelar a exclusão impede qualquer alteração física ou lógica nos dados, preservando o estado anterior; com a lista vazia, a interface deve tratar coleções sem elementos de forma elegante, permitindo novas inserções sem falhas de layout ou exceções de ponteiro nulo.

Ligação entre o ensaio e meus arquivos da atividade: O ensaio prático em memória serviu para testar a lógica de dicionários com IDs, enquanto a atividade aplicada levou esses conceitos para tabelas relacionais reais com SQLite e interface gráfica Tkinter.

Minha previsão antes da alteração guiada e o resultado observado: Previa que a edição sem critério de ID poderia duplicar registros; a implementação com `UPDATE ... WHERE id = ?` confirmou que a atualização ocorre de forma cirúrgica na linha correta.

## Continuação em casa
Arquivos/versão executados: 
Pasta e comando usados: 
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
A decisão de centralizar o CRUD de produtos na classe `RepositorioSqlite` garante que tanto a interface gráfica quanto os testes automatizados compartilhem exatamente a mesma regra de acesso ao banco. O uso de parâmetros separados protege contra falhas de sintaxe e injeção, enquanto o controle rigoroso da chave primária (ID) assegura que atualizações modifiquem o registro correto sem duplicações indesejadas. O início da gestão de clientes na mesma base consolida a estrutura relacional para as próximas etapas do projeto.

## Checklist da interface
Controles e rótulos que conferi: Campos de entrada para nome e preço/cliente, botões de ação (Salvar, Novo, Excluir), abas de Produtos e Clientes, e tabelas Treeview.
Percurso por Tab/Shift+Tab e acionamento: Navegação fluida entre os campos do formulário e botões acionáveis por Enter ou Barra de Espaço.
Mensagem após erro e possibilidade de corrigir: Mensagens de erro exibidas em alertas explicativos, mantendo os dados no formulário para correção imediata sem perda de estado.
Redimensionamento e comportamento que observei: Janela responsiva com adaptação correta dos elementos graças ao uso de pesos (`weight`) nas linhas e colunas.

## Pendências
O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência; todos os casos da matriz e testes automatizados foram executados e validados com sucesso no ambiente local.
Caso para nova tentativa em sala: