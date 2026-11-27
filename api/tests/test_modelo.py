"""Testes de desempenho e de integridade do modelo.

Executar a partir da pasta api/ com: pytest -v tests/test_modelo.py
"""

import shutil

import pytest

from config import CAMINHO_DADOS_TESTE, CAMINHO_MODELO, HASH_MODELO
from model import Avaliador, Carregador, Modelo, ModeloAdulteradoError

# Limites mínimos para aceitar um modelo. O modelo atual obteve acurácia de 0,608 e
# F1 macro de 0,586 no conjunto de teste, e a linha de base obteve 0,437 e 0,203.
LIMITE_ACURACIA = 0.58
LIMITE_F1_MACRO = 0.55


@pytest.fixture(scope="module")
def metricas() -> dict[str, float]:
    """Avalia o modelo exportado no conjunto de teste que ele nunca viu."""
    modelo = Modelo.carregar(CAMINHO_MODELO, HASH_MODELO)
    entradas, classes_reais = Carregador().carregar_dados(CAMINHO_DADOS_TESTE)
    return Avaliador().avaliar(modelo, entradas, classes_reais)


def test_acuracia_atende_limite(metricas):
    assert metricas["acuracia"] >= LIMITE_ACURACIA


def test_f1_macro_atende_limite(metricas):
    assert metricas["f1_macro"] >= LIMITE_F1_MACRO


def test_modelo_adulterado_nao_e_carregado(tmp_path):
    copia = tmp_path / CAMINHO_MODELO.name
    shutil.copy(CAMINHO_MODELO, copia)
    with open(copia, "ab") as arquivo:
        arquivo.write(b"\x00")

    with pytest.raises(ModeloAdulteradoError):
        Modelo.carregar(copia, HASH_MODELO)
