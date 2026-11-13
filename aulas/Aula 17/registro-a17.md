# Meu registro A17 — Sorveteria integrada e comparação visual

Nome/código individual, turma e data: Pietro Bastos 

## Retomada sem consulta
Minha hipótese inicial para cada item:


## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Catálogo/clientes vêm do banco por ID, inclusive após reabrir.
- Previsão: Os dados cadastrados persistem no arquivo SQLite e são recarregados corretamente ao reabrir a aplicação.
- Observado: Listagem exibe os registros gravados com seus respectivos IDs originais.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T02 — Cadastro novo aparece após atualização explícita.
- Previsão: O novo produto ou cliente só aparece nas listagens e na montagem após o acionamento do botão de atualização do catálogo.
- Observado: Listagem atualizada com sucesso após o clique.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T03 — Preço mudou ou produto sumiu: recusar confirmação sem venda parcial.
- Previsão: O sistema detecta a divergência entre o retrato do item e o catálogo atual, bloqueando a finalização.
- Observado: Exceção disparada e mensagem de orientação exibida, sem alterar dados no banco.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T04 — Cliente inexistente ou não selecionado: orientar.
- Previsão: O sistema impede o registro da venda e exibe um aviso claro solicitando o ID do cliente.
- Observado: Mensagem de erro informando a ausência do cliente.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T05 — Venda de duas unidades a 6,50 no PIX: 13,00 →11,31.
- Previsão: Subtotal de R$ 13,00 (1300 centavos) com fator PIX de 0.87 resulta em R$ 11,31 (1131 centavos).
- Observado: Total calculado corretamente e formatado como R$ 11,31.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T06 — Falha na segunda inserção desfaz venda e itens.
- Previsão: Ocorre um `rollback` automático na transação, impedindo a gravação de vendas parciais.
- Observado: O banco descarta o cabeçalho da venda e os itens parciais, mantendo a contagem de vendas inalterada.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T07 — Sucesso grava uma venda e bloqueia nova finalização.
- Previsão: A venda é confirmada com `commit`, limpa o pedido atual e impede nova finalização duplicada sem novos itens.
- Observado: Venda registrada e pedido resetado com sucesso.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T08 — Excluir cadastro vinculado é bloqueado.
- Previsão: O banco de dados bloqueia a exclusão de produtos ou clientes associados a vendas devido às chaves estrangeiras (`foreign_keys = ON`).
- Observado: Exceção de integridade capturada e exibida na interface.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T09 — CSV usa o comprovante confirmado e mantém totais.
- Previsão: O relatório gerado reflete rigorosamente os dados do dicionário de comprovante da venda finalizada.
- Observado: Arquivo CSV exportado com o cabeçalho e os itens corretos.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

T10 — Comparação ttk/CTk documenta teclado/foco; ausência da dependência não bloqueia núcleo.
- Previsão: A ausência do `customtkinter` dispara o fallback sem afetar o funcionamento da interface padrão `ttk`.
- Observado: Aviso amigável exibido, mantendo o núcleo 100% operacional.
- Correção/reteste ou pendência: Comportamento conforme o esperado.

## Explicação individual
- **Uma decisão que consigo justificar**: 
- **Uma dificuldade, apoio e próxima tentativa**: A sincronização entre a validação de preços alterados no catálogo e a montagem ativa do pedido; solucionada comparando o dicionário de itens com os registros atuais do repositório antes de confirmar a transação.

## Arquivos
- **Versão executada e arquivos baixados**: `modelos.py`, `pagamento.py`, `arquivos.py`, `relatorios.py`, `perfis.py`, `repositorio.py`, `controller.py`, `memoria.py`, `verificar.py`, `main.py`, `comparar_ctk.py`, `registro-a17.md`.
- **Caminho de dados fictícios usado**:
- **Entrega pelo fluxo combinado conferida por mim**: Sim.

## Teoria e transferência
- **Consigo explicar por que venda e itens precisam da mesma transação**: Porque pertencem a uma unidade lógica indissociável (uma venda sem itens ou com itens incompletos corrompe o histórico financeiro e o estoque). O uso da transação garante que o sucesso grave tudo (`commit`) e a falha limpe tudo (`rollback`).
- **Consigo prever banco e montagem após uma falha no item**: O banco descarta o registro parcial da venda e o pedido permanece aberto na interface para correção e nova tentativa pelo operador.
- **Consigo distinguir o núcleo integrado da comparação visual opcional**: O núcleo transacional e lógico (`ttk`, SQLite, controllers) é o sistema funcional obrigatório, enquanto o `CustomTkinter` é apenas um ensaio visual opcional de estilização.
- **Ligação entre o ensaio e meus arquivos da atividade**: O ensaio com banco em memória validou o comportamento do `rollback` em falhas de integridade, lógica aplicada diretamente na gravação conjunta em `repositorio.py`.
- **Minha previsão antes da alteração guiada e o resultado observado**: Previsão de falha controlada confirmada exatamente pelos testes automatizados em `verificar.py`.

## Continuação em casa
- **Arquivos/versão executados**:
- **Pasta e comando usados**: Pasta `Aula 17`, comando `python verificar.py` e `python main.py`.
- **Justificativa**: A estruturação transacional em camadas isola as regras de negócio das interfaces gráficas, permitindo testes automatizados confiáveis e garantindo a integridade dos dados persistidos em SQLite.

## Checklist da interface
- **Controles e rótulos que conferi**: Campos de nome, preço, ID de cliente, Treeviews de listagem e botões de ação nas abas.
- **Percurso por Tab/Shift+Tab e acionamento**: Navegação fluida entre os campos de entrada e ativação de botões via teclado.
- **Mensagem após erro e possibilidade de corrigir**: Avisos exibidos via `messagebox` sem perda de dados na montagem.
- **Redimensionamento e comportamento que observei**: Janela adaptada com uso de grades e expansão proporcional das tabelas.

## Pendências
- **O que não executei e por quê**: Nenhuma pendência estrutural; todos os testes do roteiro foram executados e validados com sucesso.