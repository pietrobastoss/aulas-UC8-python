# A17: assinaturas de apoio; traga sua implementação anterior.

class SessaoDemo:
    """Simulação local de identificação/perfil; não autentica usuários reais."""

    def __init__(self):
        self.nome = None
        self.perfil = None
        self.ativo = False

    def entrar(self, nome, perfil):
        """Registra o usuário fictício com o nome e perfil informados."""
        nome_limpo = str(nome).strip()
        perfil_limpo = str(perfil).strip()
        
        if not nome_limpo:
            raise ValueError("O nome do usuário não pode estar vazio.")
        if not perfil_limpo:
            raise ValueError("O perfil do usuário não pode estar vazio.")
            
        self.nome = nome_limpo
        self.perfil = perfil_limpo
        self.ativo = True

    def pode_configurar(self):
        """Retorna True se houver um usuário ativo com perfil administrativo/configurador."""
        if not self.ativo or not self.perfil:
            return False
        return self.perfil.lower() in ("gerente", "admin", "administrador")

    def sair(self):
        """Encerra a sessão local ativa."""
        self.nome = None
        self.perfil = None
        self.ativo = False
