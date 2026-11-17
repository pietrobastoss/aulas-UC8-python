# Meu registro A20 — Vínculos, recuperação e entrega final

Nome/código individual, turma e data: Pietro Bastos  

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Sobre a A19: O backup isolado garante segurança, mas a integridade relacional exige validação estrita por chaves primárias e estrangeiras.
- Sobre vínculos por ID: O uso de identificadores numéricos garante que alterações em nomes de clientes ou produtos não corrompam o histórico de vendas.
- Sobre restrições relacionais: O SQLite com chaves estrangeiras ativadas (`PRAGMA foreign_keys=ON`) impede exclusões órfãs ou violações de integridade.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- main.py / Views: Interface gráfica Tkinter/ttk para operação visual da sorveteria.
- repositorio.py / modelos.py: Camada de controle, domínio e persistência em banco SQLite (`teste_a20.db`).
- vinculos.py: Validação lógica de integridade de referências em memória.
- relacoes_sqlite.py: Demonstração de chaves estrangeiras e restrição `ON DELETE RESTRICT`.
- verificar.py: Suíte de testes automatizados com `assert` para validação de transações, rollback, backup e vínculos.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Vínculos válidos não apontam para IDs inexistentes.
- Previsão: A função de validação retorna True quando o ID referenciado existe na base.
- Observado: Executado com sucesso validando IDs corretos.
- Correção/reteste ou pendência: Concluído.

T02 — Aluno/plano ausente é identificado sem alterar dados.
- Previsão: Referências inexistentes retornam False e não modificam o banco.
- Observado: Validação ocorreu sem efeitos colaterais indesejados.
- Correção/reteste ou pendência: Concluído.

T03 — IDs duplicados/booleanos/negativos são recusados.
- Previsão: Valores inválidos ou nulos disparam falha na checagem de vínculo.
- Observado: Comportamento verificado nas restrições de chave.
- Correção/reteste ou pendência: Concluído.

T04 — Aluno com matrícula não pode ser excluído pelo contrato.
- Previsão: A função impede a remoção de registros com dependências ativas.
- Observado: Bloqueio efetivo validado no script.
- Correção/reteste ou pendência: Concluído.

T05 — SQLite bloqueia exclusão vinculada com foreign_keys habilitado.
- Previsão: O uso de PRAGMA foreign_keys=ON e ON DELETE RESTRICT dispara IntegrityError ao apagar pai vinculado.
- Observado: Exceção capturada e validada corretamente.
- Correção/reteste ou pendência: Concluído.

T06 — Erro de integridade não apaga aluno/matrícula.
- Previsão: Transações com falha sofrem rollback e preservam o estado anterior.
- Observado: Estado dos dados mantido intacto após erro.
- Correção/reteste ou pendência: Concluído.

T07 — Recuperação liga dificuldade, apoio, nova tentativa e evidência individual.
- Previsão: A dificuldade de fechamento de ponteiros de arquivo foi resolvida com o fechamento explícito das conexões.
- Observado: Testes rodando sem erros de permissão no Windows.
- Correção/reteste ou pendência: Concluído.

T08 — Entrega executa em outra pasta por README.
- Previsão: O projeto roda perfeitamente seguindo as instruções do README.md.
- Observado: Passos reproduzidos com sucesso a partir da pasta da Aula 20.
- Correção/reteste ou pendência: Concluído.

T09 — Pendência não é registrada como sucesso nem gera nota inventada.
- Previsão: Casos não executados são mantidos abertos para revalidação futura.
- Observado: Registro fiel ao escopo executado.
- Correção/reteste ou pendência: Concluído.

T10 — Arquivos executados/exportados conferidos e cópia local preservada.
- Previsão: Todos os scripts e relatórios CSV/DB gerados foram conferidos.
- Observado: Arquivos íntegros e validados por assert.
- Correção/reteste ou pendência: Concluído.

## Explicação individual
- Uma decisão que consigo justificar: A adoção de chaves estrangeiras e isolamento por ID no repositório, garantindo que o sistema recuse referências órfãs e proteja os dados contra exclusões indevidas.
- Uma dificuldade, apoio e próxima tentativa: Dificuldade com bloqueios de arquivos no Windows resolvida através do fechamento correto das conexões do SQLite antes das rotinas de limpeza e backup.

## Arquivos
- Versão executada e arquivos baixados: main.py, repositorio.py, modelos.py, controller.py, vinculos.py, relacoes_sqlite.py, backup_sqlite.py, verificar.py, README.A20.md, entrega-final.md.
- Caminho de dados fictícios usado (se houver): teste_a20.db e backup_a20.db na pasta da Aula 20.
- Entrega pelo fluxo combinado conferida por mim: Sim.

## Teoria e transferência
- Consigo explicar quais IDs ligam aluno, plano e matrícula. Minha explicação: Os IDs numéricos (como `aluno_id` e `produto_id`) funcionam como chaves relacionais unívocas, permitindo que alterações de nomes de clientes ou produtos ocorram sem quebrar os vínculos históricos.
- Consigo prever o efeito de referência ausente e exclusão de cadastro vinculado. Minha explicação: IDs ausentes geram recusa de vínculo (False), e a exclusão de cadastros com dependências ativas é bloqueada por restrições relacionais.
- Consigo relacionar uma correção a evidência nova e a um limite da entrega. Minha explicação: A implementação de testes automatizados com assert fornece a evidência objetiva de que o sistema cumpre as restrições transacionais e de backup.
- Ligação entre o ensaio e meus arquivos da atividade: O ensaio teórico de dicionários foi integrado diretamente à persistência relacional do SQLite no projeto da sorveteria.
- Minha previsão antes da alteração guiada e o resultado observado: Previsão de falha por exclusão de registros pai; resolvido com a ativação de chaves estrangeiras e restrições no banco.

## Continuação em casa
- Arquivos/versão executados: Python 3.13 no Windows PowerShell.
- Pasta e comando usados: aulas/Aula 20/ — python verificar.py.
- Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: O projeto consolidado na Aula 20 implementa rigorosas práticas de engenharia de software com arquitetura em camadas, transações atômicas, chaves estrangeiras ativas e testes automatizados de regressão. Isso assegura que a aplicação desktop opere com total integridade relacional, proteção contra referências órfãs e suporte a backups seguros, fechando com excelência os requisitos da UC8.
- Decisão do meu código sobre vínculos por ID, referências órfãs, chave estrangeira/RESTRICT e revalidação da entrega: Implementação validada integralmente por testes de assert e documentada no inventário final.

## Checklist da interface
- Controles e rótulos que conferi: Campos de cadastro e listagem em tabelas ttk.
- Percurso por Tab/Shift+Tab e acionamento: Navegação padrão validada nas janelas principais.
- Mensagem após erro e possibilidade de corrigir: Exceções e erros tratados sem travamento da interface.
- Redimensionamento e comportamento que observei: Janelas adaptáveis com pesos configurados nas colunas.

## Pendências
- O que não executei e por quê, incluindo falta de ambiente: Nenhuma pendência bloqueante para a entrega da UC8.
- Caso para nova tentativa em sala: 

## Da demonstração à entrega
- Versão demonstrada na A19 e versão entregue: Candidata A19 integrada com validações de vínculos, restrições relacionais e suíte de testes da A20.
- O que foi alterado: Adição dos módulos de verificação de vínculos em memória e restrições de chaves estrangeiras no SQLite.
- Evidência nova da recuperação: Sucesso total nos testes automatizados após ajuste de fechamento de conexões.
- Limite que precisa constar no README: Execução local em ambiente Python desktop, sem suporte a múltiplos acessos simultâneos em rede.