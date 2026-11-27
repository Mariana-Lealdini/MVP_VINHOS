"""Configurações da API: caminhos dos arquivos e dados de integridade do modelo."""

from pathlib import Path

PASTA_API = Path(__file__).resolve().parent
PASTA_ML = PASTA_API / "MachineLearning"

CAMINHO_MODELO = PASTA_ML / "pipelines" / "modelo_vinhos.pkl"
CAMINHO_DADOS_TESTE = PASTA_ML / "data" / "vinhos_teste.csv"

# SHA-256 gerado na seção 13 do notebook. Deve ser atualizado sempre que o modelo for trocado.
HASH_MODELO = "1496c6343d246b775b21e4ff36702add864bfa156b8fa1e604216191e3d8840b"

ATRIBUTOS = [
    "acidez_fixa",
    "acidez_volatil",
    "acido_citrico",
    "acucar_residual",
    "cloretos",
    "dioxido_enxofre_livre",
    "dioxido_enxofre_total",
    "densidade",
    "ph",
    "sulfatos",
    "alcool",
    "tipo_branco",
]
COLUNA_CLASSE = "classe"
ORDEM_CLASSES = ["baixa", "media", "alta"]
