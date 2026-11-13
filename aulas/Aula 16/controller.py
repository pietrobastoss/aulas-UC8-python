# A16: assinaturas de apoio; traga sua implementação anterior.

from pagamento import preco_para_centavos

class CadastroController:

    def __init__(self, repositorio):
        """Inicializa o controller recebendo um repositório que atenda ao contrato."""
        self.repositorio = repositorio

    def listar(self, tipo):
        """Lista os registros do tipo especificado ('produto' ou 'cliente')."""
        tipo_normalizado = str(tipo).strip().lower()
        if tipo_normalizado in ("produto", "produtos"):
            return self.repositorio.listar_produtos()
        elif tipo_normalizado in ("cliente", "clientes"):
            return self.repositorio.listar_clientes()
        else:
            raise ValueError(f"Tipo de cadastro desconhecido: '{tipo}'. Use 'produto' ou 'cliente'.")

    def salvar(self, tipo, nome, preco_texto='', codigo=None):
        """Coordena a inclusão ou edição de um produto ou cliente de acordo com a presença do código."""
        tipo_normalizado = str(tipo).strip().lower()
        
        if tipo_normalizado in ("produto", "produtos"):
            preco_centavos = preco_para_centavos(preco_texto)
            if codigo is not None and str(codigo).strip() != "":
                # Edição de produto existente
                return self.repositorio.editar_produto(codigo, nome, preco_centavos)
            else:
                # Inclusão de novo produto
                return self.repositorio.adicionar_produto(nome, preco_centavos)
                
        elif tipo_normalizado in ("cliente", "clientes"):
            if codigo is not None and str(codigo).strip() != "":
                # Edição de cliente existente
                return self.repositorio.editar_cliente(codigo, nome)
            else:
                # Inclusão de novo cliente
                return self.repositorio.adicionar_cliente(nome)
        else:
            raise ValueError(f"Tipo de cadastro desconhecido: '{tipo}'. Use 'produto' ou 'cliente'.")

    def excluir(self, tipo, codigo, confirmado):
        """Coordena a exclusão de um produto ou cliente pelo ID, respeitando a confirmação."""
        tipo_normalizado = str(tipo).strip().lower()
        
        if tipo_normalizado in ("produto", "produtos"):
            return self.repositorio.excluir_produto(codigo, confirmado=confirmado)
        elif tipo_normalizado in ("cliente", "clientes"):
            return self.repositorio.excluir_cliente(codigo, confirmado=confirmado)
        else:
            raise ValueError(f"Tipo de cadastro desconhecido: '{tipo}'. Use 'produto' ou 'cliente'.")
