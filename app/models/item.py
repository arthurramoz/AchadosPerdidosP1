from app.data.itens_mock import ITENS


class Item:
    def __init__(self, id, nome, categoria, local_encontrado, status='guardado', data_encontrado='2026-10-01'):
        self._id = id
        self.alterar_nome(nome)
        self.alterar_categoria(categoria)
        self.alterar_local(local_encontrado)
        self.alterar_status(status)
        self._data_encontrado = data_encontrado

    def mostrar_id(self):
        return self._id

    def mostrar_nome(self):
        return self._nome

    def mostrar_categoria(self):
        return self._categoria

    def mostrar_local(self):
        return self._local_encontrado

    def mostrar_status(self):
        return self._status

    def mostrar_data_encontrado(self):
        return self._data_encontrado

    def esta_disponivel(self):
        return self._status.lower() == 'guardado'

    def pertence_a_categoria(self, categoria):
        return self._categoria.lower() == categoria.lower()

    def alterar_nome(self, novo_nome):
        if not novo_nome or novo_nome.strip() == '':
            raise ValueError('nome do item não pode ser vazio')
        self._nome = novo_nome.strip()

    def alterar_categoria(self, nova_categoria):
        if not nova_categoria or nova_categoria.strip() == '':
            raise ValueError('categoria do item não pode ser vazia')
        self._categoria = nova_categoria.strip()

    def alterar_local(self, novo_local):
        if not novo_local or novo_local.strip() == '':
            raise ValueError('local encontrado não pode ser vazio')
        self._local_encontrado = novo_local.strip()

    def alterar_status(self, novo_status):
        status_limpo = novo_status.strip().lower()
        if status_limpo not in ['guardado', 'devolvido']:
            raise ValueError("status deve ser 'guardado' ou 'devolvido'")
        self._status = status_limpo

    def marcar_como_devolvido(self):
        if not self.esta_disponivel():
            raise ValueError('item já foi devolvido anteriormente')
        self.alterar_status('devolvido')

    def __repr__(self):
        return f'Item({self._nome}, status={self._status})'


def carregar_itens():
    return [
        Item(
            dados['id'],
            dados['nome'],
            dados['categoria'],
            dados['local_encontrado'],
            dados['status'],
            dados.get('data_encontrado', '2026-10-01'),
        )
        for dados in ITENS
    ]
