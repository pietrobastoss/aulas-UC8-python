# A17: assinaturas de apoio; traga sua implementação anterior.

from pagamento import preco_para_centavos

class CadastroController:
    def __init__(self, repositorio):
        """Inicializa o controller com uma referência ao repositório (memória ou SQLite)."""
        if repositorio is None:
            raise ValueError("O repositório não pode ser nulo.")
        self.repositorio = repositorio

    def listar(self, tipo):
        """Retorna a lista de registros de acordo com o tipo ('produto' ou 'cliente')."""
        t = str(tipo).strip().lower()
        if t == "produto":
            return self.repositorio.listar_produtos()
        elif t == "cliente":
            return self.repositorio.listar_clientes()
        else:
            raise ValueError(f"Tipo de cadastro desconhecido: '{tipo}'.")

    def salvar(self, tipo, nome, preco_texto='', codigo=None):
        """Coordena a inclusão (se código ausente) ou a edição (se código informado) de produtos ou clientes."""
        t = str(tipo).strip().lower()
        nome_limpo = str(nome).strip()
        
        if not nome_limpo:
            raise ValueError("O nome não pode estar vazio.")

        if t == "produto":
            # Converte o texto do preço em centavos utilizando o conversor monetário
            preco_centavos = preco_para_centavos(preco_texto)
            
            if codigo is None or str(codigo).strip() == "":
                return self.repositorio.adicionar_produto(nome_limpo, preco_centavos)
            else:
                return self.repositorio.editar_produto(codigo, nome_limpo, preco_centavos)
                
        elif t == "cliente":
            if codigo is None or str(codigo).strip() == "":
                return self.repositorio.adicionar_cliente(nome_limpo)
            else:
                return self.repositorio.editar_cliente(codigo, nome_limpo)
        else:
            raise ValueError(f"Tipo de cadastro desconhecido: '{tipo}'.")

    def excluir(self, tipo, codigo, confirmado):
        """Coordena a exclusão de um registro após confirmação explícita."""
        t = str(tipo).strip().lower()
        
        if not confirmado:
            raise ValueError("A exclusão precisa ser confirmada.")

        if t == "produto":
            return self.repositorio.excluir_produto(codigo, confirmado=True)
        elif t == "cliente":
            return self.repositorio.excluir_cliente(codigo, confirmado=True)
        else:
            raise ValueError(f"Tipo de cadastro desconhecido: '{tipo}'.")
