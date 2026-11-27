"""Configuração dos logs da API, exibidos no terminal e gravados na pasta log/."""

import logging
from logging.config import dictConfig
from pathlib import Path

PASTA_LOG = Path(__file__).resolve().parent / "log"
PASTA_LOG.mkdir(exist_ok=True)

dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "padrao": {
            "format": "[%(asctime)s] %(levelname)-7s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "padrao",
            "stream": "ext://sys.stdout",
        },
        "arquivo": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "padrao",
            "filename": str(PASTA_LOG / "api.log"),
            "maxBytes": 100_000,
            "backupCount": 5,
            "encoding": "utf-8",
            "delay": True,
        },
    },
    "root": {
        "handlers": ["console", "arquivo"],
        "level": "INFO",
    },
})

logger = logging.getLogger("api_vinhos")
