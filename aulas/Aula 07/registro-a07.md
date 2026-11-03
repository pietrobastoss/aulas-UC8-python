# Meu registro A07 — Sorveteria: produtos, itens e pedido

Nome/código individual, turma e data: Pietro Bastos

## Retomada sem consulta
Minha hipótese inicial para cada item:
- O objeto Pedido precisa conter seu próprio dicionário de itens para que múltiplos pedidos abertos na aplicação não compartilhem a mesma lista mutável.
- A validação da quantidade deve ocorrer antes de alterar o estado do pedido, preservando os itens anteriores intactos em caso de erro.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- `modelos.py`: Contém as classes `Produto` (código, nome, preço em centavos), `Item` (produto e quantidade validada) e `Pedido` (dicionário de itens e totalizador), além das funções de apoio `quantidade()` e `formatar()`.
- `verificar.py`: Importa o modelo e executa os testes automatizados via `assert` sem utilizar interface gráfica.
- `main.py`: Importa o modelo e constrói a interface gráfica em Tkinter/ttk, integrando catálogo com `Combobox` readonly, validação e listagem em `Treeview`.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Duas frutas a R$5,00 e três leites a R$7,50: subtotal 10,00 + 22,50 = 32,50.
Previsão: Total de 3250 centavos (R$ 32,50) com duas linhas de itens e subtotais corretos (1000 e 2250 centavos).
Observado: Os subtotais e o total conferiram exatamente com o esperado.
Correção/reteste ou pendência: Executado com sucesso em `verificar.py`.

T02 — Pedido novo sem itens e sem compartilhar a coleção do anterior.
Previsão: Um segundo pedido instanciado deve iniciar com dicionário de itens vazio e total 0.
Observado: O segundo pedido iniciou vazio, provando o isolamento das coleções criadas no `__init__`.
Correção/reteste ou pendência: Testado e aprovado.

T03 — Adicionar o mesmo código soma quantidades; nome igual com ID distinto continua distinto.
Previsão: Repetir o código da fruta (101) deve acumular na mesma linha do dicionário; produtos com nomes iguais mas códigos diferentes ocupam linhas separadas.
Observado: A quantidade foi acumulada corretamente na mesma linha e IDs distintos permaneceram separados.
Correção/reteste ou pendência: Concluído e verificado.

T04 — Sem seleção: orientar e preservar pedido.
Previsão: O sistema deve exibir mensagem orientativa e manter o pedido inalterado caso nenhuma opção esteja selecionada.
Observado: Mensagem exibida e pedido preservado.
Correção/reteste ou pendência: Testado na interface.

T05 — Quantidade vazia, texto, 0, negativa, decimal ou acima de 999: recusar sem alteração.
Previsão: O método `quantidade()` deve levantar `ValueError` para entradas inválidas como "abc", "-2" ou vazias, mantendo os itens anteriores intactos.
Observado: A exceção foi interceptada corretamente e os itens anteriores foram preservados.
Correção/reteste ou pendência: Validado por testes automatizados e interface.

T06 — Acumular quantidade acima de 999: preservar a linha anterior.
Previsão: Tentar acumular uma quantidade que ultrapasse 999 deve recusar a operação e manter a quantidade anterior.
Observado: Limite respeitado e valor anterior preservado.
Correção/reteste ou pendência: Concluído.

T07 — Total recalculado depois de cada inclusão válida.
Previsão: O valor total da interface deve atualizar dinamicamente a cada inclusão aceita.
Observado: Total atualizado corretamente após cada adição.
Correção/reteste ou pendência: Aprovado.

T08 — Percurso por teclado, rótulos, expansão e execução sem imagem.
Previsão: A aplicação deve permitir navegação completa via `Tab`/`Shift+Tab` e acionamento por teclado.
Observado: Navegação fluida e interface responsiva sem necessidade de mouses ou imagens.
Correção/reteste ou pendência: Executado com sucesso.

## Explicação individual
Uma decisão que consigo justificar:
A decisão de inicializar a coleção `self.itens = {}` diretamente dentro do construtor `__init__` da classe `Pedido` garante que cada pedido possua seu próprio espaço de armazenamento isolado, evitando o erro comum de compartilhar listas ou dicionários mutáveis entre instâncias diferentes.

Uma dificuldade, apoio e próxima tentativa:
A principal atenção foi garantir que a validação da quantidade acontecesse de forma estrita antes de modificar o dicionário do pedido, assegurando que uma entrada inválida não corrompesse ou apagasse dados anteriores.

## Arquivos
Versão executada e arquivos baixados: `modelos.py`, `verificar.py`, `main.py`, `registro-a07.md`
Caminho de dados fictícios usado (se houver): Catálogo local com códigos 101 (Fruta), 102 (Leite) e 103 (Chocolate).
Entrega pelo fluxo combinado conferida por mim: Sim.

## Teoria e transferência
O que são classe e instância no ensaio das caixas: Classe (`Caixa`) é o molde que define dados e ações; instância (`caixa_a`, `caixa_b`) são os objetos concretos criados a partir desse molde.
O que __init__ prepara e qual objeto self identifica: O `__init__` prepara os dados iniciais de cada objeto criado, e `self` identifica exatamente a instância específica que recebeu a chamada do método.
Por que cada pedido precisa de sua própria coleção: Para garantir o isolamento dos dados, de modo que adicionar itens em um pedido não afete o outro.
Onde ficam preço, quantidade, subtotal e total no meu código: O preço unitário fica no `Produto`, a quantidade no `Item`, o subtotal é calculado pelo método `subtotal()` do `Item`, e o total é somado no `Pedido`.
Como meu código localiza um produto pelo código: Através da busca no dicionário do catálogo ou do pedido utilizando o código numérico como chave (`codigo_produto`).
O que mudou no ensaio quando dois nomes apontaram para o mesmo objeto: Apontar duas variáveis para o mesmo objeto faz com que alterações feitas através de qualquer um dos nomes reflitam no mesmo objeto compartilhado, em vez de criar caixas independentes.

## Continuação em casa
Arquivos e versão que realmente executei: `modelos.py`, `verificar.py`, `main.py`
Comando e pasta usados: `python verificar.py` e `python main.py` na pasta `A07`.
Justificativa de 5–8 linhas ou nome do áudio de aproximadamente 60 segundos: 
A escolha de validar a quantidade e o código antes de qualquer alteração no pedido é fundamental para manter a consistência dos dados. Caso ocorra um erro de entrada, como digitar letras em vez de números, a exceção é lançada e capturada sem modificar a estrutura interna. Assim, os itens inseridos anteriormente permanecem absolutamente intactos, garantindo robustez e confiabilidade à aplicação desktop.

## Checklist da interface
Seleção identificável — observação: Catálogo exibido de forma legível em um `Combobox` no formato `[Código] Nome - Preço`.
Mensagem compreensível após erro — observação: Rótulo de aviso dedicado na parte inferior informando claramente a falha de validação sem apagar os dados.
Percurso por Tab/Shift+Tab e acionamento — observação: Navegação completa por teclado entre os campos e botões de ação.
Correção na mesma janela — observação: Permite corrigir a quantidade inválida e tentar novamente sem reiniciar a aplicação.

## O que ainda não executei
Caso pendente e motivo, incluindo falta de ambiente quando houver: Nenhum caso pendente; todos os fluxos foram testados e aprovados com sucesso.
Próxima tentativa que levarei para conferência: Exploração de novas funcionalidades de pagamento na próxima aula (A08).