"""Verificação de integridade de arquivos por hash SHA-256."""

import hashlib
from pathlib import Path

TAMANHO_BLOCO = 65_536


class ModeloAdulteradoError(Exception):
    """Indica que o hash do arquivo do modelo não corresponde ao valor esperado."""


def calcular_sha256(caminho: Path) -> str:
    """Calcula o hash SHA-256 de um arquivo, lendo-o em blocos."""
    resumo = hashlib.sha256()
    with open(caminho, "rb") as arquivo:
        for bloco in iter(lambda: arquivo.read(TAMANHO_BLOCO), b""):
            resumo.update(bloco)
    return resumo.hexdigest()


def verificar_integridade(caminho: Path, hash_esperado: str) -> None:
    """Interrompe a execução se o hash do arquivo for diferente do esperado."""
    hash_calculado = calcular_sha256(caminho)
    if hash_calculado != hash_esperado:
        raise ModeloAdulteradoError(
            f"O hash do arquivo {Path(caminho).name} não corresponde ao esperado. "
            "O modelo não foi carregado."
        )
