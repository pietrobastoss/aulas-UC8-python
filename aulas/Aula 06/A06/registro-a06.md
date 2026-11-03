# Meu registro A06 — objetos e módulos
Nome/código individual: Pietro Bastos
Turma e data: UC8 - Python · 

## Hipóteses sem consulta
- O que fica confirmado após erro na quinta nota? O último registro válido anterior permanece intacto; a tentativa com erro é rejeitada e descartada.
- Qual a diferença entre editar, confirmar e limpar? Editar altera apenas os campos visuais (Entry); confirmar valida e armazena os dados no modelo; limpar esvazia somente os widgets da tela sem tocar no objeto confirmado.
- O que aconteceria se dois nomes apontassem para o mesmo objeto? Alterar os dados por qualquer um dos nomes afetaria o mesmo registro, eliminando a independência entre instâncias.

## Arquitetura antes do código
Pasta com aluno.py, verificar_modelo.py e main.py:
- Qual arquivo contém regras? aluno.py
- Qual cria widgets? main.py
- Quem importa quem? main.py e verificar_modelo.py importam aluno.py.
- O que __init__ cria em cada nova instância? Atributos de instância independentes (nome, turma e uma nova lista self.notas = []).
- Por que duas chamadas Aluno() diferem de rui = lia? Aluno() cria instâncias distintas na memória; rui = lia faz duas variáveis apontarem para exatamente o mesmo objeto.
- O que self identifica em uma chamada de método? O objeto específico que recebeu a chamada (instância atual).

## Testes executados
- T01: Importar aluno sem Tk, sem janela e sem leitura de teclado.
  - Previsão: Módulo importa sem erros e sem abrir janelas.
  - Observado: Executado com sucesso via terminal.
  - Correção/reteste: Nenhuma correção necessária.

- T03: Lia/T1/[6,7,8,9,10] e Rui/T2/[5,5,5,5,5]; médias 8.0 e 5.0.
  - Previsão: Objetos calculam médias corretas e mantêm dados separados.
  - Observado: Médias obtidas perfeitamente (8.0 e 5.0).
  - Correção/reteste: Nenhum.

- T06: Após válido, erro na quinta nota; preservar os três atributos e resumo.
  - Previsão: O registro anterior continua salvo.
  - Observado: Mensagem de erro retornada e dados intactos preservados.
  - Correção/reteste: Nenhum.

- T12: Confirmar Lia e abrir C1; editar Rui e errar a última nota: C1 e confirmado permanecem.
  - Previsão: A consulta reflete o retrato no momento da abertura e não muda com edições inválidas.
  - Observado: Comportamento confirmado perfeitamente.
  - Correção/reteste: Nenhum.

## Explicação individual
Mostre dois objetos independentes e uma tentativa inválida após um válido. Indique a linha que confirma o conjunto e por que a interface não repete a regra. O que um assert verifica? Qual caso ainda falta?
- A confirmação ocorre ao final do método atualizar (`self.notas = notas_validadas`), após todas as verificações passarem com sucesso. A interface delega a lógica ao modelo para evitar duplicação de código. O `assert` compara uma previsão com o resultado real em testes automatizados. Todos os testes principais foram executados.

## Teoria e transferência
- Consigo apontar classe, instância, __init__ e self no exemplo.
  - Minha explicação: A classe define o modelo em `aluno.py`, `__init__` inicializa as listas exclusivas com `self.notas` para cada instância criada.
- Consigo provar que dois objetos mantêm dados independentes.
  - Minha explicação: Comprovado em `verificar_modelo.py` ao atualizar apenas `lia` e verificar que `rui` permaneceu vazio.
- Consigo explicar a direção dos imports entre modelo, verificador e interface.
  - Minha explicação: O modelo é independente (não importa Tkinter nem GUI); o verificador e a interface importam o modelo.

## Continuação em casa
-------------------------------

Justificativa de 5–8 linhas (Decisão sobre classe, instância, listas próprias, confirmação integral e separação):
A separação entre o modelo (`aluno.py`), o verificador automatizado (`verificar_modelo.py`) e a interface gráfica (`main.py`) garantiu que a lógica de negócios e as validações fossem testadas de forma independente, sem acoplar regras ao Tkinter. O uso de listas exclusivas em self.notas garantiu a independência total entre as instâncias, enquanto a confirmação integral protegeu os dados contra corrupção em caso de entradas inválidas.



## Checklist da interface
- Controles e rótulos conferidos, percurso por Tab/Shift+Tab funcional, mensagens de erro exibidas corretamente no rótulo de aviso sem travamentos, e suporte completo a execução sem a imagem opcional (`marca-a06.png`).