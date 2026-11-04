# Meu registro A09 — Catálogo e carrinho: seleção por identidade

Nome/código individual, turma e data: Pietro Bastos 

## Retomada sem consulta
Minha hipótese inicial para cada item:
- A conferência do PIX duas vezes aplica o fator e recalcula a prévia com base no subtotal atualizado.
- O arredondamento monetário utiliza `ROUND_HALF_UP` com duas casas decimais via `Decimal`.
- Diferente de uma janela filha `Toplevel` que depende da principal, a raiz `Tk` gerencia o ciclo principal de eventos do aplicativo.
- O retrato antigo de um cálculo em consultas/telas persiste até que uma nova mutação válida ocorra e redesenhe a interface.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- `modelos.py`: Contém as classes `Produto`, `Item`, `Pedido` e funções de formato/quantidade. Mantém o estado lógico em memória (dicionário indexado por código).
- `pagamento.py`: Gerencia conversões monetárias e fatores de desconto por forma de pagamento.
- `verificar.py`: Testa o modelo de forma isolada via asserções automáticas sem interface gráfica.
- `main.py`: Constrói a interface Tkinter/ttk com duas `Treeview` (Catálogo e Carrinho), mapeando o `iid` ao código único do produto e integrando as ações ao modelo.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Uma linha por código, repetição soma quantidade.
Previsão: Adicionar repetidamente o mesmo código incrementa a quantidade na mesma linha consolidada.
Observado: Linhas consolidadas corretamente por código, acumulando quantidades sem duplicar registros na tabela.
Correção/reteste ou pendência: Nenhum erro encontrado; comportamento validado no teste unitário.

T02 — Atualizar fruta para quatro com leite três: total 42,50.
Previsão: Substituir a quantidade da Fruta para 4 e manter Leite em 3 gera um subtotal de R$ 42,50 (4*10 + 3*2.50 ou conforme preços definidos).
Observado: Total calculado e exibido exatamente como previsto no modelo.
Correção/reteste ou pendência: Ajustado o mapeamento do `iid` para garantir substituição exata em vez de soma.

T03 — Remover leite: total 20,00; remover fruta: zero.
Previsão: A exclusão progressiva recalcula os subtotais e zera completamente o carrinho ao remover o último item.
Observado: Carrinho esvaziado corretamente, total zerado e interface tratada sem erros de seleção ausente.
Correção/reteste ou pendência: Validado.

T04 — Selecionar ID após mover/ordenar linhas mantém o alvo correto.
Previsão: Reordenar visualmente as linhas na tabela não altera o identificador (`iid`) vinculado ao código do produto.
Observado: A operação continuou atingindo o produto correto independentemente da nova posição visual.
Correção/reteste ou pendência: Sucesso na fixação do ID como chave de identidade.

T05 — Adicionar sem seleção de catálogo: orientação, sem mutação.
Previsão: O sistema exibe mensagem orientativa na barra de avisos e não altera o carrinho.
Observado: Aviso exibido na cor vermelha/azul orientando o usuário, mantendo o pedido inalterado.
Correção/reteste ou pendência: Tratado com `if not selecao: return`.

T06 — Atualizar/remover sem seleção de carrinho: orientação.
Previsão: O clique em atualizar ou remover sem linha selecionada exibe aviso sem quebrar a execução.
Observado: Mensagem de orientação apresentada com sucesso.
Correção/reteste ou pendência: Validado.

T07 — Quantidade inválida ou ID inexistente preserva pedido.
Previsão: Exceções de valor ou chave lançadas por entradas inválidas não corrompem o estado anterior do pedido.
Observado: Estado anterior rigorosamente preservado após a captura dos erros `ValueError` e `KeyError`.
Correção/reteste ou pendência: Blocos `try/except` implementados corretamente no controlador de ações.

T08 — Barra de rolagem, expansão, Tab e seleção no teclado.
Previsão: As tabelas comportam barras de rolagem verticais e permitem navegação fluida por teclado.
Observado: Navegação por `Tab` e rolagem operando perfeitamente.
Correção/reteste ou pendência: Configurado peso nas linhas e colunas dos frames (`grid`).

T09 — Pagamento recalculado a partir do novo subtotal.
Previsão: Alterar a forma de pagamento ou a quantidade de itens atualiza instantaneamente a prévia monetária.
Observado: Recálculo automático ativado a cada alteração de quantidade ou seleção de combobox.
Correção/reteste ou pendência: Vinculado o evento de seleção do combobox ao redesenho da interface.

## Explicação individual
Uma decisão que consigo justificar:
O uso do código do produto como `iid` na `Treeview` e chave no dicionário do `Pedido`, pois garante que a identidade do item seja mantida independentemente de ordenações visuais na tabela.

Uma dificuldade, apoio e próxima tentativa:
A principal dificuldade foi tratar corretamente o estado de carrinho vazio ao tentar realizar seleções. O apoio veio do exemplo da teoria sobre verificação de tuplas vazias em `tree.selection()`.

## Arquivos
******************
## Teoria e transferência
Consigo distinguir identidade de posição visual.
Minha explicação: Posição visual é o índice em que a linha aparece na tela (que muda ao ordenar), enquanto a identidade é o código único imutável do produto.

Consigo explicar a diferença entre adicionar, atualizar e remover.
Minha explicação: Adicionar soma unidades ao estoque existente do item; atualizar substitui diretamente a quantidade por um novo valor; remover exclui por completo o item do pedido.

Consigo prever a tela e o total ao remover o último item.
Minha explicação: A tabela fica limpa, o total exibe R$ 0,00 e o sistema evita buscar por linhas inexistentes.

Ligação entre o ensaio e meus arquivos da atividade: O ensaio validou a lógica de dicionários com chaves fixas, aplicada diretamente no modelo e na interface.
Minha previsão antes da alteração guiada e o resultado observado: A previsão de que o ID preserva o alvo correto após ordenação foi confirmada na prática.

## Continuação em casa
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: 
A adoção da identidade por código (ID) em vez da posição visual resolveu o problema de edição em listas ordenadas. O uso de dicionários no modelo permitiu atualizar e remover com precisão cirúrgica sem acoplamento à interface gráfica. O tratamento de seleções vazias evitou falhas em carrinhos limpos, assegurando robustez e estabilidade à aplicação desktop.

Decisão do meu código sobre identidade por código, iid/seleção, atualização/remoção e total derivado do modelo: Integrado de forma limpa nos arquivos entregues.


## Checklist da interface
Controles e rótulos que conferi: Catálogo, Carrinho, Entradas de Quantidade, Combobox de Pagamento e Rótulos de Totais.
Percurso por Tab/Shift+Tab e acionamento: Validado entre campos de entrada e botões.
Mensagem após erro e possibilidade de corrigir: Mensagens de aviso dinâmicas integradas sem travamento.
Redimensionamento e comportamento que observei: Janela responsiva com pesos configurados nas colunas.

