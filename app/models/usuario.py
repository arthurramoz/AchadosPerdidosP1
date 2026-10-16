from app.data.usuarios_mock import USUARIOS


class Usuario:
    LIMITE_REIVINDICACOES = 1

    def __init__(self, id, nome, cpf, senha):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_cpf(cpf)
        self._senha = senha

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_cpf(self):
        return self._cpf

    def mostrar_perfil(self):
        return type(self).__name__

    def conferir_senha(self, senha):
        return self._senha == senha

    def obter_limite_reivindicacoes(self):
        return self.LIMITE_REIVINDICACOES

    def obter_permissoes(self):
        return {
            'reivindicar': True,
            'cadastrar_item': False,
            'registrar_devolucao': False,
        }

    def alterar_nome(self, novo_nome):
        if not novo_nome or novo_nome.strip() == '':
            raise ValueError('nome do usuário não pode ser vazio')
        if len(novo_nome.strip()) < 2:
            raise ValueError('nome do usuário deve ter pelo menos 2 caracteres')
        self._nome = novo_nome.strip()

    def alterar_cpf(self, novo_cpf):
        limpo = ''.join(c for c in str(novo_cpf) if c.isdigit())
        if len(limpo) != 11:
            raise ValueError('CPF deve conter exatamente 11 dígitos numéricos')
        self._cpf = limpo

    def __repr__(self):
        return f'{self.mostrar_perfil()}({self._nome})'


class Cidadao(Usuario):
    LIMITE_REIVINDICACOES = 3

    def obter_permissoes(self):
        permissoes = super().obter_permissoes()
        return permissoes


class Funcionario(Cidadao):
    LIMITE_REIVINDICACOES = 20

    def obter_permissoes(self):
        permissoes = super().obter_permissoes()
        permissoes['cadastrar_item'] = True
        permissoes['registrar_devolucao'] = True
        return permissoes


def carregar_usuarios():
    catalogo_perfis = {
        'cidadao': Cidadao,
        'funcionario': Funcionario,
    }

    lista_usuarios = []
    for dados in USUARIOS:
        classe_usuario = catalogo_perfis[dados['perfil'].lower()]
        novo_usuario = classe_usuario(
            dados['id'], dados['nome'], dados['cpf'], dados['senha']
        )
        lista_usuarios.append(novo_usuario)

    return lista_usuarios
