"""Avaliação do desempenho do modelo em um conjunto de dados rotulado."""

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

from model.modelo import Modelo


class Avaliador:
    """Calcula as métricas usadas para aceitar ou recusar um modelo."""

    def avaliar(self, modelo: Modelo, entradas: pd.DataFrame,
                classes_reais: pd.Series) -> dict[str, float]:
        """Retorna a acurácia e o F1 macro das predições do modelo."""
        classes_previstas = modelo.prever(entradas)
        return {
            "acuracia": accuracy_score(classes_reais, classes_previstas),
            "f1_macro": f1_score(classes_reais, classes_previstas,
                                 average="macro", zero_division=0),
        }
