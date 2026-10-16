from app.models.usuario import carregar_usuarios


class AuthController:
    def __init__(self):
        self._usuarios = carregar_usuarios()

    def login(self, nome, senha):
        for usuario in self._usuarios:
            if usuario.mostrar_nome().lower() == nome.lower() and usuario.conferir_senha(senha):
                return self._para_dicionario(usuario)
        return None

    def listar(self):
        return [self._para_dicionario(u) for u in self._usuarios]

    def buscar(self, id):
        usuario = self.buscar_objeto(id)
        if usuario is None:
            return None
        return self._para_dicionario(usuario)

    def buscar_objeto(self, id):
        for usuario in self._usuarios:
            if usuario.mostrar_id() == id:
                return usuario
        return None

    def _para_dicionario(self, usuario):
        return {
            'id': usuario.mostrar_id(),
            'nome': usuario.mostrar_nome(),
            'cpf': usuario.mostrar_cpf(),
            'perfil': usuario.mostrar_perfil(),
            'limite_reivindicacoes': usuario.obter_limite_reivindicacoes(),
            'permissoes': usuario.obter_permissoes(),
        }
