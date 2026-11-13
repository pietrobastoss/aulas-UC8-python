# A16: assinaturas de apoio; traga sua implementação anterior.

class SessaoDemo:
    """Simulação local de identificação/perfil; não autentica usuários reais."""

    def __init__(self):
        self.nome = None
        self.perfil = None
        self.logado = False

    def entrar(self, nome, perfil):
        """Inicia uma sessão simulada para o usuário com um determinado perfil."""
        if not nome or not str(nome).strip():
            raise ValueError("O nome do usuário não pode estar vazio.")
        if not perfil or not str(perfil).strip():
            raise ValueError("O perfil não pode estar vazio.")
        
        self.nome = str(nome).strip()
        self.perfil = str(perfil).strip()
        self.logado = True

    def pode_configurar(self):
        """Retorna True se o usuário logado possui privilégios de configuração (ex: Administrador/Gerente)."""
        if not self.logado:
            return False
        # Perfis administrativos ou gerenciais possuem permissão de configuração
        perfis_permitidos = {"Administrador", "Gerente", "Admin", "Gestor"}
        return self.perfil in perfis_permitidos

    def sair(self):
        """Encerra a sessão atual, limpando os dados do usuário."""
        self.nome = None
        self.perfil = None
        self.logado = False