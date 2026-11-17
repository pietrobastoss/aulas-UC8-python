# A17: assinaturas de apoio; traga sua implementação anterior.

from copy import deepcopy
from repositorio import validar_nome, validar_preco, validar_id

class RepositorioMemoria:
    """Repositório volátil em memória para testes e execução sem banco de dados."""

    def __init__(self):
        self.produtos = {}
        self.clientes = {}
        self.vendas = []
        self._prox_prod_id = 1
        self._prox_cli_id = 1
        self._prox_venda_id = 1

    def adicionar_produto(self, nome, preco):
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        
        prod_id = self._prox_prod_id
        self._prox_prod_id += 1
        
        self.produtos[prod_id] = {
            "id": prod_id,
            "nome": nome_valido,
            "preco_centavos": preco_valido
        }
        return prod_id

    def listar_produtos(self):
        # Retorna cópias profundas ordenadas por ID para proteger o estado interno
        return [deepcopy(self.produtos[pid]) for pid in sorted(self.produtos.keys())]

    def editar_produto(self, codigo, nome, preco):
        cod = validar_id(codigo)
        if cod not in self.produtos:
            raise KeyError(f"Produto com ID {cod} não encontrado.")
            
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        
        self.produtos[cod]["nome"] = nome_valido
        self.produtos[cod]["preco_centavos"] = preco_valido
        return True

    def excluir_produto(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão precisa ser confirmada explicitamente.")
        if cod not in self.produtos:
            raise KeyError(f"Produto com ID {cod} não encontrado.")
            
        # Verifica se o produto está vinculado a alguma venda registrada em memória
        for venda in self.vendas:
            for item in venda.get("itens", []):
                if item.get("codigo") == cod:
                    raise RuntimeError("Não é possível excluir um produto vinculado a vendas registradas.")
                    
        del self.produtos[cod]
        return True

    def adicionar_cliente(self, nome):
        nome_valido = validar_nome(nome)
        
        cli_id = self._prox_cli_id
        self._prox_cli_id += 1
        
        self.clientes[cli_id] = {
            "id": cli_id,
            "nome": nome_valido
        }
        return cli_id

    def listar_clientes(self):
        return [deepcopy(self.clientes[cid]) for cid in sorted(self.clientes.keys())]

    def editar_cliente(self, codigo, nome):
        cod = validar_id(codigo)
        if cod not in self.clientes:
            raise KeyError(f"Cliente com ID {cod} não encontrado.")
            
        nome_valido = validar_nome(nome)
        self.clientes[cod]["nome"] = nome_valido
        return True

    def excluir_cliente(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão precisa ser confirmada explicitamente.")
        if cod not in self.clientes:
            raise KeyError(f"Cliente com ID {cod} não encontrado.")
            
        # Verifica se o cliente está vinculado a alguma venda registrada em memória
        for venda in self.vendas:
            if venda.get("cliente_id") == cod:
                raise RuntimeError("Não é possível excluir um cliente vinculado a vendas registradas.")
                
        del self.clientes[cod]
        return True

    def iniciar_vendas(self):
        """Método de suporte/compatibilidade."""
        pass

    def registrar_venda(self, cliente_id, itens, forma):
        """Registra a venda e seus itens em memória."""
        cli_id = validar_id(cliente_id)
        if cli_id not in self.clientes:
            raise ValueError(f"Cliente ID {cli_id} não cadastrado.")
        if not itens or not isinstance(itens, list):
            raise ValueError("O pedido deve conter ao menos um item válido.")

        total_geral = sum(int(item["subtotal"]) for item in itens)
        venda_id = self._prox_venda_id
        self._prox_venda_id += 1

        venda_registrada = {
            "id": venda_id,
            "cliente_id": cli_id,
            "forma_pagamento": forma,
            "total_centavos": total_geral,
            "itens": deepcopy(itens)
        }
        
        self.vendas.append(venda_registrada)
        return venda_id

    def listar_vendas(self):
        return deepcopy(self.vendas)