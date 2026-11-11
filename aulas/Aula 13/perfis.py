#A13: assinaturas de apoio; traga sua implementação anterior.
class SessaoDemo:
    
    """Simulação local de identificação/perfil; não autentica usuários reais."""

    def __init__(self):
        self.nome = None
        self.perfil = None
        self.ativo = False

    def entrar(self, nome, perfil):
        """
        Define a sessão atual com nome fictício e perfil de demonstração.
        Perfis aceitos tipicamente: 'Caixa', 'Administração'.
        """
        if not str(nome).strip():
            raise ValueError("O nome do usuário não pode ser vazio.")
        if not str(perfil).strip():
            raise ValueError("O perfil de demonstração é obrigatório.")
            
        self.nome = str(nome).strip()
        self.perfil = str(perfil).strip()
        self.ativo = True
        return True

    def pode_configurar(self):
        """
        Verifica se a sessão ativa possui autorização para configurações.
        Apenas o perfil 'Administração' possui permissão nesta simulação.
        """
        if not self.ativo:
            return False
        return self.perfil.lower() in ["administração", "administracao", "admin"]

    def sair(self):
        """Encerra e limpa a sessão fictícia ativa."""
        self.nome = None
        self.perfil = None
        self.ativo = False
        return True