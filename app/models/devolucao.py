from app.data.devolucoes_mock import DEVOLUCOES


class Devolucao:
    def __init__(self, id, item_id, usuario_id, data_devolucao, observacao):
        self._id = id
        self._item_id = item_id
        self._usuario_id = usuario_id
        self._data_devolucao = data_devolucao
        self.alterar_observacao(observacao)

    def mostrar_id(self):
        return self._id

    def mostrar_item_id(self):
        return self._item_id

    def mostrar_usuario_id(self):
        return self._usuario_id

    def mostrar_data_devolucao(self):
        return self._data_devolucao

    def mostrar_observacao(self):
        return self._observacao

    def alterar_observacao(self, nova_observacao):
        if not nova_observacao or nova_observacao.strip() == '':
            raise ValueError('observação da devolução não pode ser vazia')
        self._observacao = nova_observacao.strip()

    def __repr__(self):
        return f'Devolucao(item={self._item_id}, usuario={self._usuario_id})'


def carregar_devolucoes():
    return [
        Devolucao(
            dados['id'],
            dados['item_id'],
            dados['usuario_id'],
            dados['data_devolucao'],
            dados['observacao'],
        )
        for dados in DEVOLUCOES
    ]
