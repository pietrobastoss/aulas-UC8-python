# A02 — estados e transições do cadastro

Código do estudante: 
Arquivo e interpretador executados: exercicio01.py, exercicio02.py / Python 3.14

## Retomada sem consulta
1. O que get devolve? Por que int pode falhar?
Minha resposta inicial: O método get() devolve o valor atual do campo em formato de string (texto). O int() pode falhar gerando um ValueError se tentar converter caracteres alfabéticos ou strings vazias que não representam números inteiros válidos.

2. O que muda entre passar uma função e chamá-la ao ligar um botão?
Minha resposta inicial: Passar a função sem parênteses (ex: `command=funcao`) diz ao botão para executá-la apenas quando o usuário clicar. Colocar parênteses (ex: `command=funcao()`) executaria a função imediatamente no momento em que a interface é construída, antes de qualquer clique.

3. Que caso detecta um nome preenchido somente com espaços?
Minha resposta inicial: A validação que aplica `.strip()` no texto e verifica se o resultado é uma string vazia (`if not nome:` ou `if len(nome) == 0:`), pois o strip remove os espaços em branco das pontas.

## Preveja e depois execute (nomes sempre fictícios)
| Caso | Estado/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Registrar | Mensagem de ausência | Retornou "Nenhum cadastro registrado nesta sessão." | Nenhum |
| T02 | Registrar Lia / Costa / 18 e Exibir | Confirmação e dados exibidos | Dados aceitos e exibidos corretamente | Nenhum |
| T03 | Editar para Rui / Lima / 22; somente Exibir | Exibir mantém Lia Costa | Exibir ignorou edição e manteve o último válido | Nenhum |
| T04 | Limpar campos e depois Exibir | Campos vazios, registro mantido | Campos limpos visualmente; Exibir manteve Lia Costa | Nenhum |
| T05 | Após um válido, tentar registrar outro nome com idade abc | Erro de idade, mantém Lia | Mensagem de erro exibida; registro de Lia intacto | Nenhum |
| T06 | Registrar Rui / Lima / 22; depois Exibir | Substitui por Rui Lima | Registro atualizado com sucesso para Rui Lima, 22 anos | Nenhum |
| T07 | Nome vazio ou somente espaços | Recusa o cadastro | Exibiu erro de nome vazio; conservou anterior | Nenhum |
| T08 | Sobrenome vazio ou somente espaços | Recusa o cadastro | Exibiu erro de sobrenome vazio; conservou anterior | Nenhum |
| T09 | Idade vazia, 0, -2 e 2.5 (um teste por entrada) | Recusa todas as inválidas | Capturado pelo try/except e restrição de maior que zero | Nenhum |
| T10 | Espaços nas pontas e nome composto | Aceita e limpa as pontas | Nome normalizado corretamente com `.strip()` | Nenhum |
| T11 | Fechar, reabrir e Exibir | Memória limpa | Programa reiniciado sem registro (comportamento esperado) | Nenhum |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab: Sim, a navegação seguiu a ordem correta dos widgets.
Mensagem que precisei melhorar: Tornar o feedback de erro mais claro quando a idade informada for zero ou negativa.
Colega que testou (código fictício ou combinado): Colega fictício / Par da bancada ao lado.

## Fechamento sem consulta
Por que Limpar campos não deve apagar o registro confirmado?
Porque os campos em edição representam apenas rascunhos temporários. O registro confirmado é um estado separado e isolado que só deve ser alterado por um comando explícito de sucesso (Registrar).

Como uma tentativa inválida pode estragar um cadastro anterior se a ordem do código estiver errada?
Se o código atualizar o dicionário de registro antes de concluir todas as validações (como verificar se a idade é um inteiro válido), um erro no meio do processo pode sobrescrever parcialmente ou apagar os dados válidos anteriores.

Minha dificuldade, ajuste e próximo passo:
Dificuldade em separar mentalmente o dicionário de rascunho do dicionário de registro. O ajuste foi visualizar claramente que a função `limpar` mexe só em `campos`, enquanto `exibir` mexe só em `registro`. Próximo passo: aplicar validação e registro conjunto no conversor de moedas.