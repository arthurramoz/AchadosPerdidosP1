from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.item_routes import router as item_router
from app.routes.auth_routes import router as auth_router
from app.routes.devolucao_routes import router as devolucao_router

app = FastAPI(title='Achados e Perdidos API', version='1.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(item_router)
app.include_router(auth_router)
app.include_router(devolucao_router)


@app.get('/')
def raiz():
    return {'api': 'Achados e Perdidos', 'docs': '/docs'}
