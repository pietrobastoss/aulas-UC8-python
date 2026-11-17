# Minha sorveteria — candidata A18

## Objetivo e limites
O que está implementado e o que ainda falta:
- **Implementado:**
  - Persistência de dados de produtos, clientes e vendas utilizando banco de dados SQLite (`repositorio.py`).
  - Regras de negócio, cálculo preciso de preços e conversões monetárias utilizando `Decimal` (`modelos.py` e `pagamento.py`).
  - Gerenciamento de catálogo em JSON (`arquivos.py`), simulação de sessão e perfis de acesso (`perfis.py`) e exportação de comprovantes em CSV (`relatorios.py`).
  - Suíte de testes de regressão automatizados com `assert` (`verificar.py`), garantindo que correções aplicadas não quebrem comportamentos anteriores ou vizinhos.
  - Interface gráfica integrada construída com CustomTkinter.
- **O que ainda falta:**
  - Ajustes finos de responsividade e estilização avançada da interface para telas com resoluções muito reduzidas.

## Ambiente
Python e biblioteca gráfica usados:
- **Python:** Python 3.13
- **Biblioteca gráfica:** CustomTkinter / Tkinter nativo

Dependências efetivamente necessárias:
- `customtkinter` (interface gráfica)
- Módulos da biblioteca padrão do Python: `sqlite3`, `pathlib`, `decimal`, `json`, `csv`, `os`, `tempfile`, `contextlib`, `re`.

## Arquivos e execução
Estrutura da minha pasta:
    text
A18/
├── modelos.py         # Entidades (Produto, Item, Pedido) e regras de cálculo
├── pagamento.py       # Conversões monetárias e cálculo de descontos/taxas
├── repositorio.py     # Persistência de dados em banco SQLite
├── controller.py      # Coordenação entre a interface e o repositório
├── memoria.py         # Implementação de contrato em memória
├── arquivos.py        # Leitura, validação e escrita do catálogo JSON
├── relatorios.py      # Exportação de comprovantes de venda para CSV
├── perfis.py          # Simulação local de perfis e sessão de usuário
├── verificar.py       # Suíte de testes de regressão com assert
└── README-A18.md      # Documentação de ambiente, execução e testes