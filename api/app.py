"""API que serve o modelo de classificação da qualidade de vinhos."""

from flask import make_response, redirect
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from pydantic import ValidationError

from config import CAMINHO_MODELO, HASH_MODELO
from logger import logger
from model import Modelo, ModeloAdulteradoError, PreProcessador
from schemas import (
    ErrorSchema,
    PredicaoViewSchema,
    VinhoSchema,
    apresenta_predicao,
    campos_com_erro,
    montar_mensagem_validacao,
)

STATUS_ERRO_VALIDACAO = 422


def tratar_erro_validacao(erro: ValidationError):
    """Responde a uma entrada inválida com uma mensagem clara, sem ecoar os valores."""
    logger.warning("Entrada recusada na validação. Campos: %s",
                   ", ".join(campos_com_erro(erro)) or "corpo da requisição")
    resposta = make_response({"message": montar_mensagem_validacao(erro)})
    resposta.status_code = STATUS_ERRO_VALIDACAO
    return resposta


try:
    modelo = Modelo.carregar(CAMINHO_MODELO, HASH_MODELO)
except ModeloAdulteradoError:
    logger.critical("Falha na verificação de integridade. A API não foi iniciada.")
    raise
logger.info("Modelo carregado após a conferência do hash SHA-256.")

preprocessador = PreProcessador()

info = Info(title="API de Qualidade de Vinhos", version="1.0.0")
app = OpenAPI(
    __name__,
    info=info,
    validation_error_status=STATUS_ERRO_VALIDACAO,
    validation_error_model=ErrorSchema,
    validation_error_callback=tratar_erro_validacao,
)
app.json.sort_keys = False
app.json.ensure_ascii = False
CORS(app)

documentacao_tag = Tag(name="Documentação", description="Documentação da API no Swagger")
predicao_tag = Tag(
    name="Predição",
    description="Classificação da qualidade de um vinho a partir das medidas químicas",
)


@app.get("/", tags=[documentacao_tag])
def home():
    """Redireciona para a documentação da API."""
    return redirect("/openapi/swagger")


@app.post(
    "/predicao",
    tags=[predicao_tag],
    responses={"200": PredicaoViewSchema, "422": ErrorSchema, "500": ErrorSchema},
)
def prever_qualidade(body: VinhoSchema):
    """Classifica a qualidade de um vinho como baixa, média ou alta.

    Retorna a classe prevista e a probabilidade de cada classe.
    """
    try:
        entrada = preprocessador.preparar_entrada(body)
        classe = modelo.prever(entrada)[0]
        probabilidades = modelo.prever_probabilidades(entrada).iloc[0].to_dict()
    except Exception:
        logger.exception("Erro inesperado durante a predição.")
        return {"message": "Não foi possível realizar a predição."}, 500

    logger.info("Predição realizada com sucesso.")
    return apresenta_predicao(classe, probabilidades), 200


if __name__ == "__main__":
    app.run()
