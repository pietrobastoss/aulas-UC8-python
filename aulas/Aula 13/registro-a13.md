# Meu registro A13 — CSV de vendas e simulação de perfis

Nome/código individual, turma e data: PIETRO BASTOS

## Retomada sem consulta
Minha hipótese inicial para cada item:

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- `modelos.py`: Gerencia classes `Produto`, `Pizza`, `Bebida`, `Item` e `Pedido`, mantendo a regra de cálculo de subtotais e geração do dicionário `comprovante`.
- `pagamento.py`: Realiza conversão monetária e aplicação de fatores via `Decimal` e arredondamento `ROUND_HALF_UP`.
- `arquivos.py`: Persistência de catálogo JSON com escrita atômica (`tempfile` + `os.replace`).
- `relatorios.py`: Exportação de comprovantes confirmados para arquivos CSV utilizando codificação UTF-8 com BOM e delimitador ponto e vírgula (`;`).
- `perfis.py`: Simula sessões locais fictícias (`SessaoDemo`) com validação de perfil para controle de interface.
- `main.py`: Interface gráfica em Tkinter que integra as operações e exportações.
- `verificar.py`: Bateria de testes automatizados sem GUI validando o núcleo e as novas regras.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Sem comprovante não exporta venda fictícia.
Previsão: A função `exportar_csv` deve rejeitar o pedido antes da geração do comprovante, levantando `ValueError`.
Observado: Lançou `ValueError` conforme previsto e o arquivo de destino não foi criado.
Correção/reteste ou pendência: Validação robusta mantida na entrada de `exportar_csv`.

T02 — CSV conserva acentos e nome com separador/aspas ao ler de volta.
Previsão: O módulo `csv` com `delimiter=";"` deve encapsular o nome "Picolé; edição verão" entre aspas, permitindo leitura correta com `csv.DictReader`.
Observado: O nome foi lido de volta exatamente igual, preservando acentuação e ponto e vírgula.
Correção/reteste ou pendência: Uso de `utf-8-sig` garantiu a leitura correta dos acentos.

T03 — Quantidade, centavos e total seguem o cabeçalho documentado.
Previsão: As colunas ID, Nome, Quantidade, Preço Unitário, Subtotal, Forma de Pagamento e Total Formatado corresponderão ao dicionário do comprovante.
Observado: Todas as colunas alinharam-se perfeitamente aos dados esperados.
Correção/reteste ou pendência: Comportamento validado por `assert` no script de testes.

T04 — Relatório vem do retrato confirmado, não de Entry atuais.
Previsão: Alterações em campos de entrada da tela após a finalização não corrompem o comprovante já congelado.
Observado: O relatório gerado refletiu exclusivamente o estado do dicionário `comprovante` criado no momento do fechamento.
Correção/reteste ou pendência: Desacoplamento perfeito entre widgets de entrada e dados exportados.

T05 — Cancelar seletor preserva pedido e arquivo.
Previsão: Se o usuário cancelar a janela de salvamento de arquivos (`asksaveasfilename`), o pedido continuará intacto e nenhum arquivo será apagado.
Observado: O fluxo encerrou de forma limpa, informando o cancelamento sem alterar o estado do pedido.
Correção/reteste ou pendência: Tratamento para retorno vazio/cancelado implementado na interface.

T06 — Falha de escrita não anuncia sucesso nem substitui o destino anterior.
Previsão: Em caso de falha de permissão ou diretório inválido, a gravação atômica via arquivo temporário impede a corrupção do arquivo anterior.
Observado: A exceção foi capturada, uma mensagem de erro foi exibida e o arquivo original permaneceu inalterado.
Correção/reteste ou pendência: Uso de `tempfile.mkstemp` e `os.replace` funcionou perfeitamente.

T07 — Simulação Caixa não permite configuração no contrato de demonstração.
Previsão: O método `pode_configurar()` retornará `False` para o perfil "Caixa".
Observado: Confirmado nos testes; o acesso a menus restritos foi bloqueado logicamente.
Correção/reteste ou pendência: Lógica de perfil validada com sucesso.

T08 — Sair limpa sessão fictícia; não é exclusão de vendas.
Previsão: A chamada de `sair()` redefinirá nome e perfil para `None`, sem apagar os pedidos finalizados.
Observado: A sessão foi encerrada de forma segura, mantendo o histórico de vendas intacto.
Correção/reteste ou pendência: Estado da sessão isolado do modelo de pedidos.

T09 — Núcleo da pizzaria mantém ID, cancelamento, totais e confirmação.
Previsão: O ciclo de vida do pedido (ABERTO -> FINALIZADO) preservará o cálculo correto dos centavos.
Observado: Os subtotais e somas totais mantiveram-se precisos durante todo o ciclo.
Correção/reteste ou pendência: Regras de negócio preservadas integralmente.

## Explicação individual
Uma decisão que consigo justificar:
A adoção de escrita na exportação de relatórios CSV (`tempfile` + `os.replace`) garante que interrupções de disco ou falhas de permissão nunca corrompam um relatório exportado anteriormente.
Uma dificuldade, apoio e próxima tentativa:
Garantir que a codificação UTF-8 com BOM (`utf-8-sig`) fosse aplicada para que softwares externos de planilha reconhecessem perfeitamente os acentos e caracteres especiais em português.

## Arquivos
Versão executada e arquivos baixados: `modelos.py`, `pagamento.py`, `arquivos.py`, `relatorios.py`, `perfis.py`, `verificar.py`, `main.py`, `registro-a13.md`.
Caminho de dados fictícios usado (se houver): Diretórios temporários criados via `tempfile.TemporaryDirectory()`.
Entrega pelo fluxo combinado conferida por simulação e testes.

## Teoria e transferência
Consigo explicar a origem dos dados exportados.
Minha explicação: Os dados exportados originam-se estritamente do dicionário `comprovante` gerado e congelado no método `finalizar()` do modelo `Pedido`, isolando o relatório de modificações posteriores em campos de entrada da interface.
Consigo conferir CSV lendo nomes e valores de volta.
Minha explicação: Através do uso de `csv.DictReader` configurado com o delimitador correto (`;`), lemos o arquivo de volta e validamos se campos com pontuação e acentos mantêm a integridade das colunas.
Consigo distinguir identificação, autenticação e autorização e os limites da simulação.
Minha explicação: A identificação declara um nome fictício; a autenticação exigiria prova real de identidade (como senhas ou tokens); a autorização decide permissões (como o método `pode_configurar`). A simulação apenas exemplifica a escolha visual de um perfil.
Ligação entre o ensaio e meus arquivos da atividade: O ensaio com `StringIO` e `csv.writer` validou conceitualmente o tratamento de separadores em strings, técnica aplicada em `relatorios.py` e testada em `verificar.py`.
Minha previsão antes da alteração guiada e o resultado observado: Previa que nomes com ponto e vírgula quebrariam o relatório se concatenados manualmente, o que foi evitado com sucesso ao delegar a formatação ao módulo `csv`.

## Continuação em casa
Arquivos/versão executados: 
Pasta e comando usados: 
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decidi utilizar a escrita atômica e o módulo `csv` nativo para assegurar que caracteres especiais como ponto e vírgula sejam encapsulados corretamente em aspas sem corromper as colunas. Além disso, a separação entre identificação e autenticação reforça que a interface realiza apenas uma demonstração visual de perfis, enquanto a segurança real de um sistema exige credenciais criptografadas e validações no servidor.
Decisão do meu código sobre CSV do comprovante, leitura de volta, codificação e distinção entre identificação/autenticação/autorização: Documentada nos módulos e testes automatizados.
Minha explicação / anexo: 

## Checklist da interface
Controles e rótulos que conferi: Campos de entrada de usuário, combobox de perfis, botões de sessão e botão de exportação CSV.
Percurso por Tab/Shift+Tab e acionamento: Validado o foco sequencial entre os campos de texto, seletores e botões de ação.
Mensagem após erro e possibilidade de corrigir: Mensagens claras exibidas via `messagebox` e rótulo de aviso dinâmico, permitindo nova tentativa imediata.
Redimensionamento e comportamento que observei: Layout fluido baseado em gerenciador de grade (`grid`) com colunas expansíveis.

## Pendências
O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência em ambiente local com Python e Tkinter operacionais.
Caso para nova tentativa em sala: 