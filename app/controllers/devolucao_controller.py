from app.models.devolucao import Devolucao, carregar_devolucoes


class DevolucaoController:
    def __init__(self):
        self._devolucoes = carregar_devolucoes()

    def listar(self):
        return [self._para_dicionario(d) for d in self._devolucoes]

    def listar_por_usuario(self, usuario_id):
        devolucoes_usuario = [
            d for d in self._devolucoes if d.mostrar_usuario_id() == usuario_id
        ]
        return [self._para_dicionario(d) for d in devolucoes_usuario]

    def buscar(self, id):
        for devolucao in self._devolucoes:
            if devolucao.mostrar_id() == id:
                return self._para_dicionario(devolucao)
        return None

    def registrar_devolucao(
        self,
        item_id,
        usuario_id,
        observacao,
        item_controller,
        auth_controller,
        data_devolucao='2026-10-08',
    ):
        item = item_controller.buscar_objeto(item_id)
        if item is None:
            return 'item_nao_encontrado', None

        if not item.esta_disponivel():
            return 'item_ja_devolvido', None

        usuario = auth_controller.buscar_objeto(usuario_id)
        if usuario is None:
            return 'usuario_nao_encontrado', None

        reivindicacoes_anteriores = [
            d for d in self._devolucoes if d.mostrar_usuario_id() == usuario_id
        ]
        if len(reivindicacoes_anteriores) >= usuario.obter_limite_reivindicacoes():
            return 'limite_excedido', None

        item.marcar_como_devolvido()

        novo_id = max([d.mostrar_id() for d in self._devolucoes], default=0) + 1
        nova_devolucao = Devolucao(
            id=novo_id,
            item_id=item_id,
            usuario_id=usuario_id,
            data_devolucao=data_devolucao,
            observacao=observacao,
        )
        self._devolucoes.append(nova_devolucao)
        return 'sucesso', self._para_dicionario(nova_devolucao)

    def _para_dicionario(self, devolucao):
        return {
            'id': devolucao.mostrar_id(),
            'item_id': devolucao.mostrar_item_id(),
            'usuario_id': devolucao.mostrar_usuario_id(),
            'data_devolucao': devolucao.mostrar_data_devolucao(),
            'observacao': devolucao.mostrar_observacao(),
        }
