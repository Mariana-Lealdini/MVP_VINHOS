"""Schemas de entrada e saída da rota de predição."""

from pydantic import BaseModel, ConfigDict, Field
from pydantic.fields import FieldInfo


def medida(minimo: float, maximo: float, exemplo: float, descricao: str) -> FieldInfo:
    """Define um atributo numérico obrigatório, limitado a uma faixa plausível."""
    return Field(ge=minimo, le=maximo, strict=True, allow_inf_nan=False,
                 json_schema_extra={"example": exemplo},
                 description=f"{descricao}. Faixa aceita: {minimo:g} a {maximo:g}.")


class VinhoSchema(BaseModel):
    """Medidas químicas e tipo de um vinho a ser classificado."""

    model_config = ConfigDict(extra="forbid")

    acidez_fixa: float = medida(2, 20, 7.8, "Acidez fixa, em g/dm³ de ácido tartárico")
    acidez_volatil: float = medida(0, 2, 0.70, "Acidez volátil, em g/dm³ de ácido acético")
    acido_citrico: float = medida(0, 2, 0.05, "Ácido cítrico, em g/dm³")
    acucar_residual: float = medida(0, 70, 2.0, "Açúcar residual, em g/dm³")
    cloretos: float = medida(0, 1, 0.090, "Cloretos, em g/dm³ de cloreto de sódio")
    dioxido_enxofre_livre: float = medida(0, 300, 12.0, "Dióxido de enxofre livre, em mg/dm³")
    dioxido_enxofre_total: float = medida(0, 500, 45.0, "Dióxido de enxofre total, em mg/dm³")
    densidade: float = medida(0.98, 1.05, 0.9975, "Densidade, em g/cm³")
    ph: float = medida(2, 5, 3.40, "pH")
    sulfatos: float = medida(0, 2.5, 0.55, "Sulfatos, em g/dm³ de sulfato de potássio")
    alcool: float = medida(5, 20, 9.3, "Teor alcoólico, em % do volume")
    tipo_branco: int = Field(ge=0, le=1, strict=True, json_schema_extra={"example": 0},
                             description="Tipo do vinho: 0 para tinto e 1 para branco.")


class ProbabilidadesSchema(BaseModel):
    """Probabilidade de cada classe de qualidade."""

    baixa: float = 0.83
    media: float = 0.13
    alta: float = 0.04


class PredicaoViewSchema(BaseModel):
    """Resultado da predição devolvido ao front-end."""

    classe: str = "baixa"
    probabilidades: ProbabilidadesSchema


def faixa_do_campo(campo: str) -> tuple[float, float] | None:
    """Retorna os limites mínimo e máximo de um campo do VinhoSchema."""
    info = VinhoSchema.model_fields.get(campo)
    if info is None:
        return None
    limites = {}
    for restricao in info.metadata:
        for nome in ("ge", "le"):
            if hasattr(restricao, nome):
                limites[nome] = getattr(restricao, nome)
    if len(limites) < 2:
        return None
    return limites["ge"], limites["le"]


def apresenta_predicao(classe: str, probabilidades: dict[str, float]) -> dict:
    """Monta a resposta da predição seguindo o PredicaoViewSchema."""
    return {
        "classe": classe,
        "probabilidades": {
            nome: round(float(valor), 4) for nome, valor in probabilidades.items()
        },
    }
