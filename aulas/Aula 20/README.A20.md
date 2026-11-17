# Sistema de Sorveteria — Entrega Final (UC8)

Aplicação desktop desenvolvida em Python com interface Tkinter/ttk, estruturada em arquitetura modular por camadas (Models, Controllers, Repositório e Views), com foco em integridade transacional, relacional e testes automatizados.

## Requisitos do Ambiente
- **Python:** Versão 3.13 ou superior.
- **Bibliotecas nativas:** `tkinter`, `sqlite3`, `pathlib`, `decimal`, `json`, `csv`, `contextlib`.

## Estrutura da Pasta (Aula 20)
- `main.py` — Interface gráfica principal e ponto de entrada da aplicação.
- `repositorio.py` — Camada de persistência em banco de dados SQLite (`teste_a20.db`).
- `modelos.py` — Entidades de domínio (Produto, Item, Pedido) e cálculos com `Decimal`.
- `controller.py` — Coordenação de regras de negócio entre a interface e os dados.
- `vinculos.py` — Validação de integridade de vínculos por ID em memória.
- `relacoes_sqlite.py` — Demonstração de chaves estrangeiras e restrições relacionais (`ON DELETE RESTRICT`).
- `backup_sqlite.py` — Utilitário de segurança para cópia independente de bancos SQLite.
- `verificar.py` — Suíte de testes de regressão automatizados baseada em `assert`.
- `entrega-final.md` — Relatório detalhado e inventário da entrega.

## Como Executar o Sistema Principal
No terminal (PowerShell ou CMD) posicionado na pasta da Aula 20, execute: `python main.py`