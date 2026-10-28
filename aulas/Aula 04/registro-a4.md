# A04 — testes do sistema escolar fictício

**Código do estudante:** Pietro Bastos  
**Arquivo e interpretador executados:** `exercicio01.py`, `exercicio02.py` (Python 3.14 no VS Code)

## Retomada sem consulta
O que deve acontecer ao último registro quando a última entrada é inválida?  
**Minha resposta inicial:** O último registro confirmado deve permanecer inalterado. Apenas a mensagem de erro da tentativa atual é exibida no aviso.

O que get devolve? Como vírgula decimal é normalizada na A03?  
**Minha resposta inicial:** devolve sempre uma string (texto). vírgula decimal é feita aplicando `.strip().replace(",", ".")` antes de converter o texto para `float`.

Digitar um novo nome confirma uma nova consulta? Por quê?  
**Minha resposta inicial:** Não. Digitar altera apenas os campos em edição na janela. A consulta e o registro confirmado só são atualizados após clicar em calcular e todas as validações passarem com sucesso.

## Antes de programar
Quais valores pertencem ao mesmo registro confirmado?  
Nome, turma, a lista de notas numéricas válidas e a média calculada.

Quantidade de notas exigida e intervalo permitido:  
Exatamente 5 notas, com valores numéricos estritamente entre 0.0 e 10.0 (inclusive os limites).

Minha previsão para a média de 6, 7, 8, 9 e 10:  
8.0

Por que validar a quantidade antes de dividir?  
Para garantir que a divisão do somatório ocorra exatamente por 5, evitando divisões incorretas ou falhas de lógica caso a quantidade de itens enviada esteja errada.

## Preveja e depois execute
Use identificação e notas fictícias. Nos casos com sequência, refaça o válido indicado.
| Caso | Entrada/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Calcular média | Informar ausência de registro confirmado | Exibiu "Nenhum registro escolar confirmado nesta sessão" | Nenhum |
| T02 | Lia / T1 / notas 6, 7, 8, 9, 10 | Mensagem de sucesso e média 8.0 no painel | Mensagem de sucesso confirmada e painel com as 5 notas e média correta | Nenhum |
| T03 | Cinco notas zero, com identificação preenchida | Média 0.0 calculada e confirmada | Nota zero aceita corretamente como valor válido | Nenhum |
| T04 | Cinco notas 10, com identificação preenchida | Média 10.0 calculada e confirmada | Limite superior validado com sucesso | Nenhum |
| T05 | Notas 7,5 / 8 / 6,5 / 9 / 7; repetir usando ponto decimal | Ambas as formas aceitas e média correta | Vírgula e ponto aceitos após normalização | Nenhum |
| T06 | Após registrar T02, editar para Rui / T2 / cinco notas 5; somente Exibir | O painel continua mostrando Lia (último válido) | Painel manteve Lia intacta, ignorando a edição não calculada | Nenhum |
| T07 | Após T02, tentar Rui / T2 / 5, 5, 5, 5, abc | Mensagem de erro e preservação do registro de Lia | Erro exibido no aviso; Lia mantida no painel | Nenhum |
| T08 | Corrigir a última nota de T07 para 5 e Calcular média | Atualizar o registro para Rui com média 5.0 | Rui computado com sucesso e exibido no painel inferior | Nenhum |
| T09 | Nome vazio ou só espaços; repetir com turma vazia ou só espaços | Recusar com mensagem de erro | Erro gerado corretamente pelo `.strip()` vazio | Nenhum |
| T10 | Cada nota vazia, só espaços ou letras; uma alteração por vez | Recusar cada tentativa com erro específico | Tratamento de exceção capturou falhas individuais | Nenhum |
| T11 | Cada nota -0,1 ou 10,1; uma alteração por vez | Recusar valores fora da faixa de 0 a 10 | Mensagem de limite respeitada | Nenhum |
| T12 | Nome/turma/notas com espaços nas pontas; nome composto e acentos | Normalizar espaços e aceitar acentuação | Nomes compostos e acentos processados perfeitamente | Nenhum |
| T13 | Após um válido, Limpar campos e depois Exibir | Limpar as 7 entradas, focar no nome e manter painel | Entradas limpas com o painel anterior preservado | Nenhum |
| T14 | Notas 6 / 6 / 6 / 6 / 6,4; comparar média guardada e exibida | Média exata guardada e exibida com uma casa (`6.2`) | Float guardado bruto e apresentado formatado | Nenhum |
| T15 | No terminal, lista com quatro notas e depois seis; uma tentativa por vez | Recusar ambas as quantidades na função `calcular` | Mensagem de exigência de exatamente 5 notas exibida | Nenhum |
| T16 | Fechar, reabrir e Exibir | Iniciar sem nenhum registro confirmado | Janela iniciou limpa conforme esperado | Nenhum |

## Uso da interface
Percorri nome, turma, cinco notas e botões com Tab/Shift+Tab: Sim, navegação em ordem lógica por todos os 7 campos e botões.  
Acionei um botão usando o teclado: Sim, utilizando a barra de espaço com o foco no botão "Calcular média".  
Conferi rótulos e redimensionamento:   
Mensagem que precisei melhorar: Mensagem de erro da 5ª nota ajustada para especificar claramente o intervalo numérico permitido.  
Colega que testou (código combinado): 

## Fechamento sem consulta
Qual a diferença entre sum(notas) e len(notas)?  
`sum()` soma todos os elementos numéricos da lista, enquanto `len()` retorna a quantidade de itens presentes nela.

Por que uma lista nova de números ajuda a preservar a confirmação?  
mantendo os dados da tentativa isolados até que toda a validação esteja completa

Qual dado o painel deve mostrar se eu editar a quinta nota sem calcular?  
O último conjunto confirmado anteriormente

Formatar com uma casa muda a média guardada?  
Não. altera apenas a apresentação visual (string)

Minha dificuldade, ajuste e próxima tentativa:  
Um pouco de dificuldade na lógica de como fazer rodar direitinho mas depois de algumas tentativas deu tudo certo.

Entregas: exercicio01.py, exercicio02.py + registro.