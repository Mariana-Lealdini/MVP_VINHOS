"""Carga do conjunto de teste exportado pelo notebook."""

from pathlib import Path

import pandas as pd

from config import ATRIBUTOS, COLUNA_CLASSE


class Carregador:
    """Lê o CSV de teste e separa as entradas da classe correta."""

    def carregar_dados(self, caminho: Path) -> tuple[pd.DataFrame, pd.Series]:
        """Retorna as entradas (X) e as classes reais (y) do arquivo informado."""
        dados = pd.read_csv(caminho)
        return dados[ATRIBUTOS], dados[COLUNA_CLASSE]
