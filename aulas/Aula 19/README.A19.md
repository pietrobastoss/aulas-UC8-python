# Sistema de Sorveteria — Academia e Demonstrações Individuais (Aula 19)

Aplicação desktop desenvolvida em Python com interface Tkinter/ttk, estruturada em arquitetura modular por camadas (Models, Controllers, Repositório e Views), com foco em transações atômicas, isolamento em banco de dados SQLite e rotinas de backup seguro.

## Requisitos do Ambiente
- **Python:** Versão 3.13 ou superior.
- **Bibliotecas nativas:** `tkinter`, `sqlite3`, `pathlib`, `decimal`, `json`, `csv`, `contextlib`.

## Estrutura da Pasta (Aula 19)
- `main.py` — Interface gráfica principal e ponto de entrada da aplicação.
- `repositorio.py` — Camada de persistência em banco de dados SQLite (`teste_a19.db`) com isolamento transacional (Rollback).
- `modelos.py` — Entidades de domínio (Produto, Item, Pedido) e cálculos com `Decimal`.
- `controller.py` — Coordenação de regras de negócio entre a interface e os dados.
- `backup_sqlite.py` — Utilitário de segurança para cópia independente de bancos SQLite (`origem.backup(destino)`).
- `verificar.py` — Suíte de testes de regressão automatizados baseada em `assert` para transações e backup.
- `registro-a19.md` — Relatório individual e matriz de evidências da academia e demonstração da A19.

## Como Executar o Sistema Principal
No terminal (PowerShell ou CMD) posicionado na pasta da Aula 19, execute:
`python main.py`