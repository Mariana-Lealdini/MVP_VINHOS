"""Conversão dos dados recebidos pela API para o formato esperado pelo modelo."""

import pandas as pd

from config import ATRIBUTOS
from schemas.vinho_schema import VinhoSchema


class PreProcessador:
    """Prepara a entrada de um vinho para a predição."""

    def preparar_entrada(self, vinho: VinhoSchema) -> pd.DataFrame:
        """Monta um DataFrame de uma linha com os atributos na ordem usada no treino."""
        return pd.DataFrame([vinho.model_dump()], columns=ATRIBUTOS)
