import inspect
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient

from app.models.usuario import Usuario, Cidadao, Funcionario, carregar_usuarios
from app.models.item import Item, carregar_itens
from app.models.devolucao import Devolucao, carregar_devolucoes
from app.controllers.item_controller import ItemController
from app.controllers.auth_controller import AuthController
from app.controllers.devolucao_controller import DevolucaoController
from main import app


def check_01_hierarquia_classes():
    assert issubclass(Cidadao, Usuario), "Cidadao deve herdar de Usuario"
    assert issubclass(Funcionario, Cidadao), "Funcionario deve herdar de Cidadao"
    assert issubclass(Funcionario, Usuario), "Funcionario deve ser subclasse indireta de Usuario"
    print("[PASSOU] 01. Hierarquia com 3 classes e 2 níveis validada")


def check_02_sobrescrita_com_super():
    fonte_funcionario = inspect.getsource(Funcionario.obter_permissoes)
    assert 'super().obter_permissoes()' in fonte_funcionario, (
        "Funcionario.obter_permissoes() deve chamar super().obter_permissoes()"
    )
    print("[PASSOU] 02. Método sobrescrito com super() estendendo comportamento da base validado")


def check_03_constante_de_classe():
    assert hasattr(Usuario, 'LIMITE_REIVINDICACOES'), "Usuario deve possuir constante LIMITE_REIVINDICACOES"
    assert hasattr(Cidadao, 'LIMITE_REIVINDICACOES'), "Cidadao deve possuir constante LIMITE_REIVINDICACOES"
    assert hasattr(Funcionario, 'LIMITE_REIVINDICACOES'), "Funcionario deve possuir constante LIMITE_REIVINDICACOES"
    assert Cidadao.LIMITE_REIVINDICACOES != Funcionario.LIMITE_REIVINDICACOES, (
        "Constante de classe deve ter valor diferente nas classes filhas"
    )
    assert Cidadao.LIMITE_REIVINDICACOES == 3
    assert Funcionario.LIMITE_REIVINDICACOES == 20
    print("[PASSOU] 03. Constante de classe com valores polimórficos nas filhas validada")


def check_04_mapeamento_perfis_sem_if():
    fonte_carregar = inspect.getsource(carregar_usuarios)
    assert 'catalogo_perfis' in fonte_carregar or 'PERFIS' in fonte_carregar, (
        "Deve existir dicionário no estilo PERFIS/catalogo_perfis"
    )
    assert 'if dados' not in fonte_carregar and 'if perfil' not in fonte_carregar, (
        "Não deve haver if checando perfil ao carregar usuários"
    )
    usuarios = carregar_usuarios()
    tipos = {type(u) for u in usuarios}
    assert Cidadao in tipos and Funcionario in tipos, "Mock deve carregar instâncias de Cidadao e Funcionario"
    print("[PASSOU] 04. Mapeamento de texto do mock para classes via dicionário sem if validado")


def check_05_polimorfismo_permissoes():
    cidadao = Cidadao(100, "Teste Cidadao", "12345678901", "senha123")
    funcionario = Funcionario(101, "Teste Funcionario", "98765432100", "senha456")

    perm_cidadao = cidadao.obter_permissoes()
    perm_func = funcionario.obter_permissoes()

    assert perm_cidadao['reivindicar'] is True
    assert perm_cidadao['cadastrar_item'] is False
    assert perm_cidadao['registrar_devolucao'] is False

    assert perm_func['reivindicar'] is True
    assert perm_func['cadastrar_item'] is True
    assert perm_func['registrar_devolucao'] is True
    print("[PASSOU] 05. Polimorfismo de permissões respondendo sem if validado")


def check_06_encapsulamento_atributos_protegidos():
    item = Item(1, "Guarda-Chuva", "Acessórios", "Pátio Central")
    usuario = Cidadao(1, "Arthur", "11122233344", "123")
    devolucao = Devolucao(1, 1, 1, "2026-10-08", "Devolvido ao dono")

    assert hasattr(item, '_id') and hasattr(item, '_nome') and hasattr(item, '_status')
    assert hasattr(usuario, '_id') and hasattr(usuario, '_nome') and hasattr(usuario, '_cpf') and hasattr(usuario, '_senha')
    assert hasattr(devolucao, '_id') and hasattr(devolucao, '_item_id') and hasattr(devolucao, '_observacao')

    assert item.mostrar_id() == 1
    assert item.mostrar_nome() == "Guarda-Chuva"
    assert usuario.mostrar_nome() == "Arthur"
    assert devolucao.mostrar_id() == 1
    print("[PASSOU] 06. Encapsulamento com atributos protegidos (_) e métodos mostrar_ validado")


def check_07_sem_alterar_id_nem_mostrar_senha():
    for cls in [Item, Devolucao, Usuario, Cidadao, Funcionario]:
        assert not hasattr(cls, 'alterar_id'), f"{cls.__name__} NÃO pode ter método alterar_id"
    assert not hasattr(Usuario, 'mostrar_senha'), "Usuario NUNCA deve expor mostrar_senha"
    assert not hasattr(Cidadao, 'mostrar_senha')
    assert not hasattr(Funcionario, 'mostrar_senha')
    print("[PASSOU] 07. Regra rígida: nenhum alterar_id e senha protegida sem método de leitura")


def check_08_construtor_chama_alterar():
    fonte_item = inspect.getsource(Item.__init__)
    assert 'self.alterar_nome' in fonte_item
    assert 'self.alterar_local' in fonte_item

    fonte_usuario = inspect.getsource(Usuario.__init__)
    assert 'self.alterar_nome' in fonte_usuario
    assert 'self.alterar_cpf' in fonte_usuario

    fonte_devolucao = inspect.getsource(Devolucao.__init__)
    assert 'self.alterar_observacao' in fonte_devolucao
    print("[PASSOU] 08. Construtores chamando métodos alterar_ para garantir validação validado")


def check_09_regras_negocio_raise_valueerror():
    erros_capturados = 0

    try:
        Item(1, "   ", "Acessórios", "Pátio")
    except ValueError:
        erros_capturados += 1

    try:
        Item(1, "Chave", "Acessórios", "   ")
    except ValueError:
        erros_capturados += 1

    try:
        Item(1, "Chave", "Acessórios", "Pátio", status="perdido_na_rua")
    except ValueError:
        erros_capturados += 1

    try:
        Cidadao(1, "A", "11122233344", "123")
    except ValueError:
        erros_capturados += 1

    try:
        Cidadao(1, "Arthur Ramos", "12345", "123")
    except ValueError:
        erros_capturados += 1

    item_dev = Item(1, "Celular", "Eletrônicos", "Lab 1", status="guardado")
    item_dev.marcar_como_devolvido()
    try:
        item_dev.marcar_como_devolvido()
    except ValueError:
        erros_capturados += 1

    try:
        Devolucao(1, 1, 1, "2026-10-08", "   ")
    except ValueError:
        erros_capturados += 1

    assert erros_capturados >= 4, f"Esperado no mínimo 4 regras com raise ValueError, capturadas {erros_capturados}"
    print(f"[PASSOU] 09. Regras de negócio com raise ValueError validadas ({erros_capturados} regras testadas)")


def check_10_metodo_repr_todas_classes():
    item = Item(1, "Mouse", "Eletrônicos", "Lab 2")
    user = Cidadao(1, "Arthur", "11122233344", "123")
    dev = Devolucao(1, 1, 1, "2026-10-08", "Entregue")

    assert "Mouse" in repr(item)
    assert "Cidadao" in repr(user) and "Arthur" in repr(user)
    assert "Devolucao" in repr(dev)
    print("[PASSOU] 10. Método __repr__ implementado em todas as classes")


def check_11_camadas_models_sem_fastapi():
    import app.models.usuario as mod_usuario
    import app.models.item as mod_item
    import app.models.devolucao as mod_devolucao

    for mod in [mod_usuario, mod_item, mod_devolucao]:
        fonte = inspect.getsource(mod).lower()
        assert 'fastapi' not in fonte, f"models/{mod.__name__} NÃO pode importar FastAPI"
        assert 'httpexception' not in fonte, f"models/{mod.__name__} NÃO pode importar HTTPException"
    print("[PASSOU] 11. Camada Models 100% pura: sem nenhuma dependência do FastAPI ou HTTP")


def check_12_camadas_controllers_sem_fastapi():
    import app.controllers.item_controller as mod_ic
    import app.controllers.auth_controller as mod_ac
    import app.controllers.devolucao_controller as mod_dc

    for mod in [mod_ic, mod_ac, mod_dc]:
        fonte = inspect.getsource(mod).lower()
        assert 'fastapi' not in fonte, f"controllers/{mod.__name__} NÃO pode importar FastAPI"
        assert 'httpexception' not in fonte, f"controllers/{mod.__name__} NÃO pode importar HTTPException"
    print("[PASSOU] 12. Camada Controllers 100% desacoplada de HTTP")


def check_13_compreensao_de_lista_controllers():
    import app.controllers.item_controller as mod_ic
    fonte = inspect.getsource(mod_ic.ItemController.listar_disponiveis)
    assert '[' in fonte and 'for ' in fonte and 'in ' in fonte, (
        "ItemController.listar_disponiveis deve utilizar compreensão de lista"
    )
    print("[PASSOU] 13. Filtros com compreensão de lista nos controllers validados")


def check_14_controllers_retornam_none_ou_lista():
    ic = ItemController()
    assert ic.buscar(999999) is None, "Controller deve retornar None quando não encontra"
    assert ic.listar_por_categoria("categoria_inexistente_xyz") == [], (
        "Controller deve retornar lista vazia quando filtro não encontra nada"
    )
    print("[PASSOU] 14. Controllers devolvem None ou lista vazia, nunca códigos HTTP")


def check_15_rotas_api_codigos_http():
    client = TestClient(app)

    resp = client.get('/api/itens')
    assert resp.status_code == 200, f"Esperado 200, recebido {resp.status_code}"
    assert len(resp.json()) >= 5

    resp = client.get('/api/itens/1')
    assert resp.status_code == 200
    resp_404 = client.get('/api/itens/9999')
    assert resp_404.status_code == 404

    resp_disp = client.get('/api/itens/disponiveis')
    assert resp_disp.status_code == 200
    assert all(i['status'] == 'guardado' for i in resp_disp.json())

    novo_item_payload = {
        "nome": "Calculadora HP 12C",
        "categoria": "Eletrônicos",
        "local_encontrado": "Auditório Master"
    }
    resp_post_item = client.post('/api/itens', json=novo_item_payload)
    assert resp_post_item.status_code == 201, f"Esperado 201, recebido {resp_post_item.status_code}"
    novo_item_id = resp_post_item.json()['id']

    resp_item_invalido = client.post('/api/itens', json={
        "nome": "   ",
        "categoria": "Eletrônicos",
        "local_encontrado": "Auditório"
    })
    assert resp_item_invalido.status_code == 422, f"Esperado 422, recebido {resp_item_invalido.status_code}"

    resp_login = client.post('/api/auth/login', json={"nome": "Arthur Ramos", "senha": "art123"})
    assert resp_login.status_code == 200
    assert resp_login.json()['perfil'] == 'Cidadao'

    resp_login_err = client.post('/api/auth/login', json={"nome": "Arthur Ramos", "senha": "errada"})
    assert resp_login_err.status_code == 401

    devolucao_payload = {
        "item_id": novo_item_id,
        "usuario_id": 1,
        "observacao": "Proprietário apresentou nota fiscal da calculadora."
    }
    resp_dev = client.post('/api/devolucoes', json=devolucao_payload)
    assert resp_dev.status_code == 201, f"Esperado 201, recebido {resp_dev.status_code}"

    resp_dev_conflito = client.post('/api/devolucoes', json=devolucao_payload)
    assert resp_dev_conflito.status_code == 409, f"Esperado 409 (conflito de estado), recebido {resp_dev_conflito.status_code}"

    resp_hist = client.get('/api/usuarios/1/devolucoes')
    assert resp_hist.status_code == 200
    assert len(resp_hist.json()) >= 1

    print("[PASSOU] 15. Rotas HTTP testadas com TestClient (200, 201, 401, 404, 409 e 422)")


if __name__ == '__main__':
    print("=" * 70)
    print(" BATERIA DE VERIFICAÇÃO AUTOMATIZADA: SISTEMA ACHADOS E PERDIDOS")
    print("=" * 70)

    checks = [
        check_01_hierarquia_classes,
        check_02_sobrescrita_com_super,
        check_03_constante_de_classe,
        check_04_mapeamento_perfis_sem_if,
        check_05_polimorfismo_permissoes,
        check_06_encapsulamento_atributos_protegidos,
        check_07_sem_alterar_id_nem_mostrar_senha,
        check_08_construtor_chama_alterar,
        check_09_regras_negocio_raise_valueerror,
        check_10_metodo_repr_todas_classes,
        check_11_camadas_models_sem_fastapi,
        check_12_camadas_controllers_sem_fastapi,
        check_13_compreensao_de_lista_controllers,
        check_14_controllers_retornam_none_ou_lista,
        check_15_rotas_api_codigos_http,
    ]

    for check in checks:
        check()

    print("=" * 70)
    print(" TODOS OS 15 TESTES PASSARAM COM 100% DE SUCESSO!")
    print(" PROJETO TOTALMENTE EM CONFORMIDADE COM A RUBRICA DA PROVA 1 (POO)!")
    print("=" * 70)
