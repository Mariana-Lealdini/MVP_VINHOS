"""Schema de erro e tradução dos erros de validação para mensagens claras."""

from pydantic import BaseModel, ValidationError

from schemas.vinho_schema import faixa_do_campo

MENSAGEM_CORPO_INVALIDO = (
    "O corpo da requisição deve ser um JSON com as 12 medidas do vinho."
)


class ErrorSchema(BaseModel):
    """Define como uma mensagem de erro é representada."""

    message: str = "ph: informe um valor entre 2 e 5."


def descrever_erro(campo: str, tipo_erro: str) -> str:
    """Converte um erro do Pydantic em uma mensagem curta sobre o campo."""
    if tipo_erro == "missing":
        return f"{campo}: campo obrigatório."
    if tipo_erro == "extra_forbidden":
        return f"{campo}: campo não reconhecido."
    if campo == "tipo_branco":
        return "tipo_branco: informe 0 para tinto ou 1 para branco."
    faixa = faixa_do_campo(campo)
    if faixa is not None:
        minimo, maximo = faixa
        return f"{campo}: informe um valor entre {minimo:g} e {maximo:g}."
    return f"{campo}: valor inválido."


def montar_mensagem_validacao(erro: ValidationError) -> str:
    """Junta em uma única mensagem os problemas encontrados em cada campo."""
    mensagens = []
    for detalhe in erro.errors():
        if not detalhe["loc"]:
            return MENSAGEM_CORPO_INVALIDO
        mensagem = descrever_erro(str(detalhe["loc"][0]), detalhe["type"])
        if mensagem not in mensagens:
            mensagens.append(mensagem)
    return " ".join(mensagens)


def campos_com_erro(erro: ValidationError) -> list[str]:
    """Lista apenas os nomes dos campos recusados, sem os valores enviados."""
    return sorted({str(detalhe["loc"][0]) for detalhe in erro.errors() if detalhe["loc"]})
