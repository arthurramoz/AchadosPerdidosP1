from app.models.item import Item, carregar_itens


class ItemController:
    def __init__(self):
        self._itens = carregar_itens()

    def listar(self):
        return [self._para_dicionario(item) for item in self._itens]

    def listar_disponiveis(self):
        itens_disponiveis = [item for item in self._itens if item.esta_disponivel()]
        return [self._para_dicionario(item) for item in itens_disponiveis]

    def listar_por_categoria(self, categoria):
        itens_categoria = [
            item for item in self._itens if item.pertence_a_categoria(categoria)
        ]
        return [self._para_dicionario(item) for item in itens_categoria]

    def buscar(self, id):
        item = self.buscar_objeto(id)
        if item is None:
            return None
        return self._para_dicionario(item)

    def buscar_objeto(self, id):
        for item in self._itens:
            if item.mostrar_id() == id:
                return item
        return None

    def cadastrar(self, nome, categoria, local_encontrado, data_encontrado='2026-10-08'):
        novo_id = max([item.mostrar_id() for item in self._itens], default=0) + 1
        novo_item = Item(
            id=novo_id,
            nome=nome,
            categoria=categoria,
            local_encontrado=local_encontrado,
            status='guardado',
            data_encontrado=data_encontrado,
        )
        self._itens.append(novo_item)
        return self._para_dicionario(novo_item)

    def relatorio_status(self):
        guardados = [item for item in self._itens if item.esta_disponivel()]
        devolvidos = [item for item in self._itens if not item.esta_disponivel()]
        return {
            'total_itens': len(self._itens),
            'guardados': len(guardados),
            'devolvidos': len(devolvidos),
        }

    def _para_dicionario(self, item):
        return {
            'id': item.mostrar_id(),
            'nome': item.mostrar_nome(),
            'categoria': item.mostrar_categoria(),
            'local_encontrado': item.mostrar_local(),
            'status': item.mostrar_status(),
            'data_encontrado': item.mostrar_data_encontrado(),
        }
