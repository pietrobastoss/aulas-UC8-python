# A03 — testes do conversor fictício

Código do estudante: Pietro
Arquivo e interpretador executados: Python 3.14 / VS Code Terminal (`exercicio01.py` e `exercicio02.py`)

## Retomada sem consulta
O que Exibir deve ler quando os campos foram editados sem confirmação?
 O dicionário de registro confirmado, ignorando o conteúdo atual das caixas de texto editáveis.

Por que um erro não pode alterar parte do último registro válido?
 Para evitar corromper o histórico com dados parciais ou misturados de tentativas inválidas.

O que get devolve? Por que int não serve para uma idade escrita como 2.5?
 Devolve uma string (`str`). O int falha porque espera um número inteiro e lança `ValueError` ao encontrar um ponto decimal.

## Antes de programar
Unidade das cotações: R$ por USD e R$ por EUR (reais por unidade de moeda estrangeira).
Operação escolhida para converter reais; justificativa por unidades: Divisão (reais ÷ cotação), pois agrupa o montante total pelo preço unitário de cada moeda.
Quais entradas e resultados precisam pertencer à mesma tentativa? O valor em reais, as duas cotações utilizadas e os dois resultados calculados (dólares e euros).

## Preveja e depois execute
As cotações desta tabela são fictícias. Mantenha a ordem quando o caso indicar.
| Caso | Entrada/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Calcular | Mensagem de ausência | Exibiu "Nenhuma conversão confirmada" | Nenhum |
| T02 | Calcular reais 100, cotação USD 5 e EUR 4 | Sucesso: $20.00 e €25.00 | Registrado e exibido corretamente com 2 casas | Nenhum |
| T03 | Editar para 200 / 10 / 8; somente Exibir | Exibir mantém valores antigos (100 / 5 / 4) | Painel não mudou até recalcular | Nenhum |
| T04 | Após T02, Calcular com 200 / 10 / abc | Erro de conversão, registro preservado | Mensagem de erro exibida; dados anteriores intactos | Nenhum |
| T05 | Corrigir para 200 / 10 / 8 e Calcular | Sucesso: $20.00 e €25.00 atualizados | Substituiu o conjunto inteiro perfeitamente | Nenhum |
| T06 | Calcular com 100,50 / 5 / 4; repetir com 100.50 | Ambos aceitos e resultados iguais | Vírgula e ponto tratados com sucesso | Nenhum |
| T07 | Calcular com 0 / 5 / 4 | Sucesso com resultados zero | $ 0.00 e € 0.00 calculados sem erro | Nenhum |
| T08 | Reais negativos; cada cotação 0 e negativa, um teste por campo | Erro em cada tentativa | Mensagens de validação barraram a atualização | Nenhum |
| T09 | Cada campo vazio, só espaços ou abc, um por vez | Erro de conversão numérico | Valores inválidos rejeitados com sucesso | Nenhum |
| T10 | Texto 1.000,50 ou 1,000.50; depois 1000,50 sem milhares | Recusa formatos com milhares; aceita sem milhares | Formatos mistos geraram ValueError corretamente | Nenhum |
| T11 | Após um válido, Limpar campos e depois Exibir | Campos vazios, registro visível | O resultado anterior continuou visível após limpar | Nenhum |
| T12 | Calcular com 10 / 3 / 6; observar arredondamento de exibição | Exibição com 2 casas, memória completa | Precisão mantida no registro, formatada na tela | Nenhum |
| T13 | Fechar, reabrir e Exibir | Janela limpa, sem registro anterior | Sessão reiniciada do zero conforme esperado | Nenhum |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab: Sim, a navegação ocorreu de cima para baixo nos campos e botões.
Usei o teclado para acionar um botão: Sim, utilizei a tecla Enter/Espaço nos botões.
Mensagem que precisei melhorar: Tornar mais explícito o aviso de que o erro não alterou os dados anteriores.
Colega que testou (código combinado): a confirmar 

## Fechamento sem consulta
Por que a cotação precisa ser maior que zero, mas o valor em reais pode ser zero?
Porque o valor em reais representa saldo disponível (que pode ser nulo), enquanto a cotação atua como divisor, e a divisão por zero ou por números negativos não possui definição matemática lógica para o câmbio.

Como evitar mostrar uma entrada atual com um resultado anterior?
Separando estritamente os campos de edição do dicionário de registro confirmado, fazendo a função de exibição ler exclusivamente os dados validados juntos.

Formatar com duas casas muda o número guardado no registro?
Não. A formatação (`:.2f`) altera apenas a representação visual em string para exibição, preservando o valor numérico completo em ponto flutuante na memória.

Minha dificuldade, correção e próximo passo:
Dificuldade inicial no tratamento de formatos decimais com vírgula, resolvida aplicando `.replace(",", ".")` antes da conversão para float. Próximo passo: aplicar validações semelhantes em sistemas com múltiplos campos na próxima aula.

Entregas: exercicio01.py, exercicio02.py e este registro preenchido.