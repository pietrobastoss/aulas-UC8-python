# A16: assinaturas de apoio; traga sua implementação anterior.

from copy import deepcopy
from repositorio import validar_nome, validar_preco, validar_id

class RepositorioMemoria:

    def __init__(self):
        self._produtos = {}  # Mapeia id -> {"id": id, "nome": nome, "preco_centavos": preco}
        self._clientes = {}  # Mapeia id -> {"id": id, "nome": nome}
        self._contador_produtos = 1
        self._contador_clientes = 1

    def adicionar_produto(self, nome, preco):
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        
        produto_id = self._contador_produtos
        self._contador_produtos += 1
        
        novo_produto = {
            "id": produto_id,
            "nome": nome_valido,
            "preco_centavos": preco_valido
        }
        self._produtos[produto_id] = novo_produto
        return deepcopy(novo_produto)

    def listar_produtos(self):
        # Retorna lista ordenada por ID, com cópias profundas para proteger o estado interno
        return [
            deepcopy(self._produtos[pid])
            for pid in sorted(self._produtos.keys())
        ]

    def editar_produto(self, codigo, nome, preco):
        cod = validar_id(codigo)
        nome_valido = validar_nome(nome)
        preco_valido = validar_preco(preco)
        
        if cod not in self._produtos:
            raise KeyError(f"Produto com ID {cod} não encontrado para edição.")
        
        produto_atualizado = {
            "id": cod,
            "nome": nome_valido,
            "preco_centavos": preco_valido
        }
        self._produtos[cod] = produto_atualizado
        return deepcopy(produto_atualizado)

    def excluir_produto(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão do produto precisa ser confirmada.")
        
        if cod not in self._produtos:
            raise KeyError(f"Produto com ID {cod} não encontrado para exclusão.")
        
        del self._produtos[cod]
        return True

    def adicionar_cliente(self, nome):
        nome_valido = validar_nome(nome)
        
        cliente_id = self._contador_clientes
        self._contador_clientes += 1
        
        novo_cliente = {
            "id": cliente_id,
            "nome": nome_valido
        }
        self._clientes[cliente_id] = novo_cliente
        return deepcopy(novo_cliente)

    def listar_clientes(self):
        return [
            deepcopy(self._clientes[cid])
            for cid in sorted(self._clientes.keys())
        ]

    def editar_cliente(self, codigo, nome):
        cod = validar_id(codigo)
        nome_valido = validar_nome(nome)
        
        if cod not in self._clientes:
            raise KeyError(f"Cliente com ID {cod} não encontrado para edição.")
        
        cliente_atualizado = {
            "id": cod,
            "nome": nome_valido
        }
        self._clientes[cod] = cliente_atualizado
        return deepcopy(cliente_atualizado)

    def excluir_cliente(self, codigo, confirmado=False):
        cod = validar_id(codigo)
        if not confirmado:
            raise ValueError("A exclusão do cliente precisa ser confirmada.")
        
        if cod not in self._clientes:
            raise KeyError(f"Cliente com ID {cod} não encontrado para exclusão.")
        
        del self._clientes[cod]
        return True
