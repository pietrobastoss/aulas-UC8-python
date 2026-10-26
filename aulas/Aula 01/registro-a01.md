# A01 — minha tentativa e meus testes

Use código de estudante na entrega. Não inclua dados pessoais de terceiros.
Python observado: Python 3.14.0
Tcl/Tk observado: 8.6
Interpretador selecionado no VS Code: .venv (Python 3.14.0)

## Diagnóstico sem consulta
1. O que distingue texto de número? O texto é tratado como caractere e armazena strings, enquanto o número permite operações matemáticas diretas.
2. Como uma função recebe uma entrada e produz uma saída? Recebe dados através de argumentos ou parâmetros e produz uma saída usando return ou atualizando elementos na interface.
3. O que uma condição decide? Decide qual bloco de código será executado com base na veracidade de uma expressão lógica (True ou False).
Minha resposta inicial: O texto aceita concatenação e o número aceita contas; funções recebem valores por parâmetros e devolvem com return; condições avaliam se algo é verdadeiro para executar um bloco.

## Matriz de testes (preencha antes e depois da execução)
| Nome fictício | Idade digitada | Resultado esperado | Resultado observado | Ajuste |
|---|---|---|---|---|
| Lia | 18 | Sucesso | Sucesso: Nome e Idade exibidos | Nenhum |
| vazio | 18 | Erro no nome | Mensagem de nome vazio | Adicionado .strip() e validação |
| somente espaços | 18 | Erro no nome | Mensagem de nome em branco | Verificação not nome_limpo |
| Lia | vazio | Erro na idade | Mensagem de erro por valor inválido | Tratamento com ValueError |
| Lia | abc | Erro na idade | Mensagem de erro por conversão | Tratamento com ValueError |
| Lia | 0 | Erro na idade | Mensagem de idade maior que zero | Validação idade <= 0 |
| Lia | -2 | Erro na idade | Mensagem de idade maior que zero | Validação idade <= 0 |
| Lia | 2.5 | Erro na idade | Mensagem de erro por não ser inteiro | Tratamento com ValueError |
| Ana Maria | 21 | Sucesso | Sucesso: Nome composto aceito | Nenhum |

## Interface
Testei botão, Tab e Shift+Tab: O foco mudou corretamente entre os campos de entrada e o botão acionou a função.
Comparei o resultado do terminal com o da janela: O terminal exibia as mensagens em texto corrido e a janela atualizou o componente de rótulo (Label) interativamente.
Fechei e reabri; o que aconteceu com o resultado? O estado anterior foi perdido e a interface voltou ao texto inicial da sessão, sem gravação permanente.

## Fechamento (sem consulta)
Explique entrada → validação → resposta com suas palavras: O programa captura o texto digitado nos campos (entrada), aplica as restrições e regras lógicas de formato e valor (validação) e exibe uma orientação ou sucesso na interface (resposta).
Uma dificuldade, a correção que tentei e meu próximo passo: A dificuldade foi tratar conversões de decimais ou letras na idade sem quebrar o programa; a correção foi utilizar blocos try-except ValueError; o próximo passo será adicionar botões de limpar e persistência na memória.
Arquivos anexados separadamente: exercicio01.py e exercicio02.py.