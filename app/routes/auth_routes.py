from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.controllers.auth_controller import AuthController

router = APIRouter(prefix='/api/auth', tags=['auth'])
controller = AuthController()


class LoginRequest(BaseModel):
    nome: str
    senha: str


@router.post('/login')
def login(credenciais: LoginRequest):
    usuario_logado = controller.login(credenciais.nome, credenciais.senha)
    if usuario_logado is None:
        raise HTTPException(401, 'nome ou senha inválidos')
    return usuario_logado


@router.get('/usuarios')
def listar_usuarios():
    return controller.listar()


@router.get('/usuarios/{id}')
def buscar_usuario(id: int):
    usuario = controller.buscar(id)
    if usuario is None:
        raise HTTPException(404, 'usuário não encontrado')
    return usuario
