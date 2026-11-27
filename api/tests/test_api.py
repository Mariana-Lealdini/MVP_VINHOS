"""Testes das rotas da API.

Executar a partir da pasta api/ com: pytest -v tests/test_api.py
"""

import pytest

from app import app
from config import ORDEM_CLASSES


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def vinho_tinto() -> dict:
    """Vinho 1 da seção 14 do notebook, classificado como baixa com 83%."""
    return {
        "acidez_fixa": 7.8,
        "acidez_volatil": 0.70,
        "acido_citrico": 0.05,
        "acucar_residual": 2.0,
        "cloretos": 0.090,
        "dioxido_enxofre_livre": 12.0,
        "dioxido_enxofre_total": 45.0,
        "densidade": 0.9975,
        "ph": 3.40,
        "sulfatos": 0.55,
        "alcool": 9.3,
        "tipo_branco": 0,
    }


def test_home_redireciona_para_documentacao(client):
    resposta = client.get("/")
    assert resposta.status_code == 302
    assert "/openapi" in resposta.location


def test_predicao_retorna_classe_e_probabilidades(client, vinho_tinto):
    resposta = client.post("/predicao", json=vinho_tinto)
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados["classe"] in ORDEM_CLASSES
    assert list(dados["probabilidades"]) == ORDEM_CLASSES
    assert sum(dados["probabilidades"].values()) == pytest.approx(1, abs=0.001)


def test_predicao_igual_a_do_notebook(client, vinho_tinto):
    dados = client.post("/predicao", json=vinho_tinto).get_json()

    assert dados["classe"] == "baixa"
    assert dados["probabilidades"]["baixa"] == pytest.approx(0.83, abs=0.01)


@pytest.mark.parametrize("campo, valor", [
    ("ph", 7.0),
    ("alcool", 2.0),
    ("densidade", 1.5),
    ("acidez_volatil", -0.1),
])
def test_valor_fora_da_faixa_e_recusado(client, vinho_tinto, campo, valor):
    resposta = client.post("/predicao", json={**vinho_tinto, campo: valor})

    assert resposta.status_code == 422
    assert campo in resposta.get_json()["message"]


@pytest.mark.parametrize("valor", [2, "1", True, 0.5])
def test_tipo_do_vinho_aceita_apenas_0_ou_1(client, vinho_tinto, valor):
    resposta = client.post("/predicao", json={**vinho_tinto, "tipo_branco": valor})

    assert resposta.status_code == 422
    assert "tipo_branco" in resposta.get_json()["message"]


@pytest.mark.parametrize("valor", ["doze", "12.5", None, True])
def test_valor_que_nao_e_numero_e_recusado(client, vinho_tinto, valor):
    resposta = client.post("/predicao", json={**vinho_tinto, "alcool": valor})

    assert resposta.status_code == 422
    assert "alcool" in resposta.get_json()["message"]


def test_numero_inteiro_e_aceito_nas_medidas(client, vinho_tinto):
    resposta = client.post("/predicao", json={**vinho_tinto, "alcool": 9})
    assert resposta.status_code == 200


def test_campo_ausente_e_recusado(client, vinho_tinto):
    del vinho_tinto["ph"]
    resposta = client.post("/predicao", json=vinho_tinto)

    assert resposta.status_code == 422
    assert "ph: campo obrigatório" in resposta.get_json()["message"]


def test_campo_desconhecido_e_recusado(client, vinho_tinto):
    resposta = client.post("/predicao", json={**vinho_tinto, "nome": "Vinho X"})
    assert resposta.status_code == 422


def test_corpo_que_nao_e_json_e_recusado(client):
    resposta = client.post("/predicao", data="texto", content_type="application/json")
    assert resposta.status_code == 422


def test_resposta_de_erro_nao_repete_o_valor_enviado(client, vinho_tinto):
    resposta = client.post("/predicao", json={**vinho_tinto, "ph": 123.456})
    assert "123.456" not in resposta.get_data(as_text=True)
