# A05 — organização e consultas do sistema escolar

**Código do estudante:** Pietro Bastos

**Arquivos e interpretador executados:**

- escolar_grupos.py
- escolar_janelas.py
- Python pelo terminal do VS Code.

## Retomada sem consulta

**Quais dados devem ficar juntos no último registro válido?**

Nome, turma, as cinco notas e a média calculada.

**Por que uma quinta nota inválida não pode alterar o nome confirmado?**

Porque todos os dados precisam ser validados antes de atualizar o registro. Se alguma nota estiver errada, o último resultado válido continua salvo.

**O que o botão recebe em command e quando essa função é executada?**

O command recebe o nome da função que será executada quando o botão for clicado. Não usamos parênteses porque queremos que ela seja executada somente no clique.

## Antes de programar

**Desenho dos pais:**

Tk → Frame base → grupos de identificação, notas e ações → campos e botões.

**Onde cada grid organiza seus filhos?**

Cada grid organiza os elementos dentro do seu próprio pai. Por exemplo, os campos de nome e turma ficam dentro do grupo de identificação.

**Diferença entre edição, registro confirmado e retrato da consulta:**

A edição é o que está digitado nos campos. O registro confirmado guarda os últimos dados calculados corretamente. O retrato da consulta mostra os dados que estavam confirmados quando a segunda janela foi aberta.

## Preveja e depois execute

| Caso | Previsão |
|---|---|
| T01 | Os campos e botões ficam separados em grupos. |
| T02 | A média das cinco notas é 8,0. |
| T03 | Aparece uma mensagem informando que não existe registro. |
| T04 | Abre a consulta C1 com os dados de Lia. |
| T05 | A consulta C1 continua mostrando Lia, mesmo com os campos alterados. |
| T06 | A nota inválida impede a atualização do registro confirmado. |
| T07 | O novo cálculo de Rui atualiza o registro principal, mas C1 continua com os dados antigos. C2 mostra Rui. |
| T08 | Os campos ficam vazios, mas o último registro continua salvo. |
| T09 | C1 fecha sem encerrar a janela principal ou C2. |
| T10 | Escape fecha somente a consulta aberta. |
| T11 | O X fecha somente a janela de consulta. |
| T12 | As validações impedem notas inválidas e aceitam vírgula ou ponto decimal. |
| T13 | É possível navegar pelos controles e observar a expansão dos campos. |
| T14 | Sem a imagem, aparece o cabeçalho textual. |
| T15 | Uma imagem válida aparece; uma imagem ausente ou inválida usa o texto alternativo. |
| T16 | O programa procura a imagem na pasta do próprio script. |
| T17 | Fechar a janela principal encerra o programa e as consultas. |

## Imagem local (opcional)

**O programa funcionou sem imagem:** Sim.

**Se criei PNG próprio:** Não criei, utilizei o cabeçalho textual.

**Qual objeto conserva a referência da imagem?**

O próprio rótulo, através de `rotulo.image = imagem`, mantém a referência para que a imagem não desapareça.

## Fechamento sem consulta

**Por que criar outra Tk/mainloop não é o contrato desta aula?**

Porque o programa já possui uma janela principal. Para abrir outra janela, usamos Toplevel, que funciona junto com a janela principal.

**Por que C1 pode manter o registro antigo depois de um novo válido?**

Porque o texto da consulta é obtido no momento em que a janela é aberta. Assim, mesmo que outro registro seja confirmado depois, a consulta antiga continua mostrando os dados anteriores.

**Qual janela cada fechamento destrói?**

O botão Fechar, o Escape e o X destroem somente a janela de consulta. A janela principal continua funcionando.

**Minha dificuldade, correção e próxima tentativa:**

Minha maior dificuldade foi organizar as funções e prestar atenção na indentação, principalmente nos callbacks dos botões. Corrigi a organização do código e consegui executar o programa. Na próxima atividade, quero prestar mais atenção na estrutura das funções para evitar erros.

## Teoria e transferência

**Consigo identificar o pai e a grade de um campo. Minha explicação:**

Sim. Cada campo pertence a um grupo, como o campo Nome, que fica dentro do grupo Identificação. O grid organiza a posição dos elementos dentro desse grupo.

**Consigo explicar sticky e peso de coluna no redimensionamento. Minha explicação:**

O sticky determina como o elemento ocupa o espaço disponível. Já o weight define quais colunas recebem mais espaço quando a janela aumenta.

**Consigo distinguir edição, confirmado e retrato da consulta. Minha explicação:**

A edição é o que está nos campos, o confirmado é o último cálculo válido e o retrato é uma cópia dos dados no momento em que a consulta foi aberta.

**Ligação entre o ensaio e meus arquivos da atividade:**

Nos dois arquivos utilizei funções separadas. No escolar_grupos.py, trabalhei principalmente com a divisão dos campos em grupos. No escolar_janelas.py, aproveitei essa estrutura e acrescentei uma segunda janela para consultar os dados.

**Minha previsão antes da alteração guiada e o resultado observado:**

Eu esperava que a organização em grupos deixasse a interface mais fácil de entender. Depois das alterações, consegui separar identificação, notas e botões, além de abrir uma segunda janela para consultar o resultado.

## Continuação em casa

**Arquivos/versão executados:**

escolar_grupos.py e escolar_janelas.py.

**Pasta e comando usados:**


**Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:**

Escolhi organizar a janela usando grupos separados para identificação, notas e ações, porque assim fica mais fácil visualizar cada parte do sistema. Também utilizei funções para separar os cálculos das ações da interface. Na consulta, usei Toplevel para abrir uma segunda janela sem precisar criar outro programa principal. Os dados da consulta são obtidos no momento em que ela é aberta, mantendo as informações antigas mesmo depois de um novo cálculo. Também deixei a opção de fechar a consulta pelo botão, pelo X ou pela tecla Escape.

**Decisão do meu código sobre hierarquia de pais, expansão dos grupos, retratos e fechamento da Toplevel:**

Utilizei Frame e LabelFrame para organizar os elementos, grid para posicionar os campos e columnconfigure para permitir a expansão. Na consulta, utilizei Toplevel e destroy() para fechar somente a segunda janela.

## Checklist da interface

**Controles e rótulos que conferi:**

Campos de nome, turma e cinco notas; botões Calcular média, Consultar e Limpar campos.

**Percurso por Tab/Shift+Tab e acionamento:**

Ainda preciso conferir a navegação por teclado.

**Mensagem após erro e possibilidade de corrigir:**

O programa apresenta mensagens de validação e permite corrigir os campos.

**Redimensionamento e comportamento que observei:**

Ainda preciso conferir melhor o comportamento dos campos ao aumentar a janela.

## Pendências

Ainda preciso testar individualmente as múltiplas consultas, o fechamento independente, a navegação por teclado, a imagem inválida e a execução a partir de outra pasta.

**Caso para nova tentativa em sala:**

Testar duas consultas abertas com registros diferentes, alterar os campos sem calcular e verificar se cada janela mantém seu próprio resultado.