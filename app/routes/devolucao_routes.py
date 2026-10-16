from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.devolucao_controller import DevolucaoController
from app.routes.item_routes import controller as item_controller
from app.routes.auth_routes import controller as auth_controller

router = APIRouter(tags=['devolucoes'])
controller = DevolucaoController()


class DevolucaoCriacaoRequest(BaseModel):
    item_id: int
    usuario_id: int
    observacao: str


@router.get('/api/devolucoes')
def listar_devolucoes():
    return controller.listar()


@router.get('/api/devolucoes/{id}')
def buscar_devolucao(id: int):
    devolucao = controller.buscar(id)
    if devolucao is None:
        raise HTTPException(404, 'devolução não encontrada')
    return devolucao


@router.post('/api/devolucoes', status_code=201)
def registrar_devolucao(dados: DevolucaoCriacaoRequest):
    try:
        status, resultado = controller.registrar_devolucao(
            item_id=dados.item_id,
            usuario_id=dados.usuario_id,
            observacao=dados.observacao,
            item_controller=item_controller,
            auth_controller=auth_controller,
        )

        if status == 'item_nao_encontrado':
            raise HTTPException(404, 'item não encontrado')
        if status == 'usuario_nao_encontrado':
            raise HTTPException(404, 'usuário não encontrado')
        if status == 'item_ja_devolvido':
            raise HTTPException(409, 'o item informado já foi devolvido anteriormente')
        if status == 'limite_excedido':
            raise HTTPException(422, 'limite de reivindicações do perfil atingido')

        return resultado
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.get('/api/usuarios/{usuario_id}/devolucoes')
def listar_devolucoes_usuario(usuario_id: int):
    usuario = auth_controller.buscar(usuario_id)
    if usuario is None:
        raise HTTPException(404, 'usuário não encontrado')
    return controller.listar_por_usuario(usuario_id)
