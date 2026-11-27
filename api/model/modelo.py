"""Carga do modelo exportado pelo notebook e realização das predições."""

import pickle
from pathlib import Path

import pandas as pd
from sklearn.pipeline import Pipeline

from config import ORDEM_CLASSES
from model.integridade import verificar_integridade


class Modelo:
    """Pipeline de classificação de vinhos (padronização seguida do KNN)."""

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    @classmethod
    def carregar(cls, caminho: Path, hash_esperado: str) -> "Modelo":
        """Carrega o pipeline de um arquivo .pkl, somente se o hash for o esperado."""
        verificar_integridade(caminho, hash_esperado)
        with open(caminho, "rb") as arquivo:
            pipeline = pickle.load(arquivo)
        return cls(pipeline)

    def prever(self, entradas: pd.DataFrame) -> list[str]:
        """Retorna a classe prevista para cada vinho."""
        return list(self.pipeline.predict(entradas))

    def prever_probabilidades(self, entradas: pd.DataFrame) -> pd.DataFrame:
        """Retorna a probabilidade de cada classe, na ordem baixa, média e alta."""
        probabilidades = pd.DataFrame(
            self.pipeline.predict_proba(entradas),
            columns=self.pipeline.classes_,
            index=entradas.index,
        )
        return probabilidades[ORDEM_CLASSES]
