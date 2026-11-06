# Meu registro A12 — Mercado: navegação e catálogo em JSON

Nome/código individual, turma e data: Pietro

## Retomada sem consulta
Minha hipótese inicial para cada item:

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

- T01 — Ausente retorna coleção vazia sem criar arquivo silenciosamente.

    Previsão: A função ler_catalogo deve retornar [] e o arquivo não deve ser gerado no disco.

    Observado: Comportamento confirmado pelo teste automatizado T01 sem criação de resíduos.

    Correção/reteste ou pendência: Nenhuma alteração necessária; passou de primeira.

- T02 — UTF-8 conserva Picolé/limão.

    Previsão: O arquivo salvo e relido com codificação UTF-8 preserva acentuações textuais perfeitamente.

    Observado: A string "Picolé de Limão" foi recuperada de forma idêntica.

    Correção/reteste ou pendência: Nenhuma pendência.

- T03 — JSON malformado e conteúdo com encoding inválido não são sobrescritos.

    Previsão: Uma exceção de sintaxe é disparada e os bytes originais do arquivo corrompido permanecem inalterados.

    Observado: O teste de comparação de bytes antes e depois da leitura falha confirmou a preservação integral.

    Correção/reteste ou pendência: Concluído com sucesso.

- T04 — Estrutura incorreta, IDs repetidos e preço inválido são rejeitados.

    Previsão: A função validar_catalogo levanta ValueError ao encontrar IDs duplicados, tipos errados ou preços negativos.

    Observado: As exceções foram lançadas e capturadas corretamente pelo bloco de teste.

    Correção/reteste ou pendência: Nenhuma pendência.

- T05 — Falha de escrita mantém o destino anterior e não anuncia sucesso.

    Previsão: Se ocorrer um erro de IO ou interrupção durante a escrita atômica, o arquivo temporário é limpo e o original preservado.

    Observado: O arquivo de destino permaneceu íntegro e mensagens de sucesso indevidas foram evitadas.

    Correção/reteste ou pendência: Aprovado nos testes.

- T06 — Cancelar seletor não altera tela nem arquivo.

    Previsão: Cancelar o filedialog retorna vazio, mantendo a interface e o estado atual intocados.

    Observado: Ação de cancelamento tratada de forma limpa na interface sem disparar exceções.

    Correção/reteste ou pendência: Concluído.

- T07 — Navegar entre abas conserva pedido e estado.

    Previsão: Alternar entre a aba do Pedido e a aba do Catálogo JSON não reinicia o pedido devido à instância única.

    Observado: O carrinho e os subtotais continuaram intactos após alternar as abas do Notebook.

    Correção/reteste ou pendência: Aprovado na interface e no teste T06 de verificação.

- T08 — Exercício JSON não modifica automaticamente o catálogo em memória.

    Previsão: Carregar um arquivo JSON na segunda aba apenas exibe seu conteúdo no widget de texto, sem sobrescrever o pedido ativo.

    Observado: Separação correta entre o repositório de catálogo e o carrinho de compras do usuário.

    Correção/reteste ou pendência: Concluído.

## Explicação individual
Uma decisão que consigo justificar:

Uma dificuldade, apoio e próxima tentativa:
ajustar a tipagem para que o construtor da classe Item aceitasse tanto textos de entrada quanto inteiros diretos gerou confusão no cálculo de itens repetidos. O apoio veio ao isolar a lógica de conversão e validar a integridade no modelo de dados.

## Arquivos
Versão executada e arquivos baixados:
Caminho de dados fictícios usado (se houver):
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo distinguir caminho, texto, codificação e dados decodificados.
Minha explicação: Sim. O caminho (Path) aponta o local no disco; o texto bruto é lido com uma codificação específica (utf-8); a decodificação (json.loads) transforma esse texto em estruturas de dados nativas do Python (listas e dicionários).
Consigo explicar por que validar JSON exige mais que aceitar a sintaxe.
Minha explicação: Um arquivo pode ter sintaxe JSON perfeitamente válida (ex: uma lista de números ou strings), mas violar completamente as regras de negócio do domínio, como exigir chaves específicas (id, nome, preco_centavos), IDs positivos únicos e preços não negativos.
Consigo prever pedido e edição depois de navegar, cancelar ou falhar na leitura.
Minha explicação: Sim. Navegar preserva os dados por causa da referência compartilhada da instância; cancelar diálogos retorna sem efeitos colaterais; falhas de leitura geram exceções tratadas que mantêm o arquivo original intacto.

Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: 
Decisão do meu código sobre leitura/escrita UTF-8, estrutura JSON, validação integral e navegação sem recriar o modelo:
Minha explicação / anexo:
A adoção de leitura e escrita com UTF-8 explícito assegura que caracteres acentuados típicos do português sejam gravados sem perdas. A validação integral estrutural separa a legibilidade do arquivo das regras estritas do domínio comercial. Além disso, a arquitetura com uma única instância de pedido acoplada ao Notebook do Tkinter impede que a troca de abas destrua o progresso do usuário, garantindo uma experiência robusta e confiável.

## Checklist da interface
Controles e rótulos que conferi: Campos de ID, Nome, Preço em centavos e Quantidade na aba de Pedido; botões de carregar e salvar JSON na aba de Catálogo.
Percurso por Tab/Shift+Tab e acionamento: Todos os campos de entrada e botões aceitam foco por teclado e acionamento via Enter/Space.
Mensagem após erro e possibilidade de corrigir: Exibição de messagebox informativa permitindo corrigir os dados imediatamente na mesma tela sem travamentos.
Redimensionamento e comportamento que observei: Janela configurada com pesos de linha e coluna (columnconfigure/rowconfigure), mantendo o layout proporcional ao redimensionar.

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
