# Minha entrega final — A20

Identificação individual e data: Pietro Bastos 
Versão/pasta enviada e cópia local: Pasta "Aula 20" (cópia de ensaio isolada preservando a estrutura anterior)

## Inventário
Arquivos necessários, README e caminho do banco fictício: 
- main.py, repositorio.py, modelos.py, backup_sqlite.py, verificar.py, vinculos.py, relacoes_sqlite.py, README.md
- Banco de dados de teste: teste_a20.db e backup_a20.db localizados na pasta da aula.
Relatórios e matriz que acompanham a entrega:
- Geração de comprovantes em CSV (teste_comprovante.csv) e matriz de registros nas folhas A19 e A20.
Ambientes/caches/dados operacionais excluídos:
- Exclusão automatizada de arquivos temporários, caches e diretórios `__pycache__` residuais do Python via rotina de limpeza do script de verificação.

## Evidências individuais
I1 — ambiente e reprodução: caso, resultado e pendência:
- Caso: Execução do script `verificar.py` no terminal Python 3.13 do Windows PowerShell. Resultado: 100% de sucesso nos asserts. Pendência: Nenhuma.
I2 — código e funcionalidades: caso, resultado e pendência:
- Caso: Transações atômicas com rollback em caso de falha de ID e isolamento de persistência. Resultado: Rollback operando perfeitamente e impedindo gravações parciais. Pendência: Nenhuma.
I3 — interface, usabilidade e acessibilidade: caso, resultado e acessibilidade:
- Caso: Navegação por teclado (Tab/Shift+Tab) nas telas Tkinter/ttk e fallback para CustomTkinter. Resultado: Comportamento responsivo validado. Pendência: Nenhuma.
I4 — eventos e validações: caso, resultado e validação:
- Caso: Tratamento de exceções para arquivos inexistentes ou sobrescrita negada de backup. Resultado: Mensagens claras exibidas e exceções disparadas conforme o contrato. Pendência: Nenhuma.

## Recuperação
Dificuldade delimitada e apoio recebido:
- Dificuldade com travamentos de ponteiros de arquivos no Windows (`PermissionError`) ao limpar bancos abertos. Apoio recebido através da análise de fechamento explícito de conexões do SQLite antes do encerramento.
Nova tentativa individual e evidência:
- Implementação de fechamento preventivo das instâncias de repositório e uso de blocos de tentativa/exceção seguros para remoção de arquivos. Evidência: Testes executados sem erros de permissão.
O que ainda não foi observado:


## Vínculos
IDs válidos, referência inexistente e exclusão vinculada:
- Matrículas e pedidos apontam estritamente para chaves primárias (IDs). Referências inexistentes retornam `False` ou geram exceções de integridade. A exclusão de cadastros vinculados é rigidamente bloqueada.
Diferença observada entre validação JSON e restrição SQLite:
- A validação em memória (JSON/dicionários) confere chaves antes de persistir, enquanto a restrição em banco de dados (`PRAGMA foreign_keys = ON` com `ON DELETE RESTRICT`) garante a integridade relacional diretamente a nível de persistência no SQLite.

## Entrega
Downloads/arquivos executados conferidos:
- Sim, todos os arquivos executados e validados por assert.
Recebimento no canal combinado conferido por mim:
- Sim, repositório e arquivos organizados conforme o fluxo acordado.
Autoavaliação e próximo estudo:
- Aprendizado sólido sobre arquitetura em camadas, persistência atômica, integridade por ID e testes automatizados em Python. Próximo estudo voltado a frameworks web e APIs.

## Conferência em pasta limpa
Comando executado pelo README:
- `python verificar.py`
Dados fictícios e caminho realmente usados:
- `teste_a20.db` e `backup_a20.db` gerados no diretório de execução da Aula 20.
Resultado do fluxo válido e da recusa:
- Sucesso no fluxo de vendas/pedidos válidos e recusa estrita ao tentar inserir IDs inexistentes ou sobrescrever backups existentes.
Correção demonstrada e evidência da nova tentativa:
- Fechamento de conexões abertas, garantindo a substituição limpa dos arquivos de banco de dados entre os testes.
Limite que outro usuário precisa conhecer:
- O ambiente requer Python 3.13 e as bibliotecas padrão do ecossistema Tkinter/SQLite nativas, sem dependências de pacotes externos obrigatórios (CustomTkinter opcional).