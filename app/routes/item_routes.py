from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.item_controller import ItemController

router = APIRouter(prefix='/api/itens', tags=['itens'])
controller = ItemController()


class ItemCriacaoRequest(BaseModel):
    nome: str
    categoria: str
    local_encontrado: str


@router.get('')
def listar():
    return controller.listar()


@router.get('/disponiveis')
def listar_disponiveis():
    return controller.listar_disponiveis()


@router.get('/relatorio/status')
def relatorio_status():
    return controller.relatorio_status()


@router.get('/categoria/{categoria}')
def listar_por_categoria(categoria: str):
    itens = controller.listar_por_categoria(categoria)
    if not itens:
        raise HTTPException(404, 'nenhum item encontrado nesta categoria')
    return itens


@router.get('/{id}')
def buscar(id: int):
    item = controller.buscar(id)
    if item is None:
        raise HTTPException(404, 'item não encontrado')
    return item


@router.post('', status_code=201)
def cadastrar(dados: ItemCriacaoRequest):
    try:
        novo_item = controller.cadastrar(
            nome=dados.nome,
            categoria=dados.categoria,
            local_encontrado=dados.local_encontrado,
        )
        return novo_item
    except ValueError as e:
        raise HTTPException(422, str(e))
