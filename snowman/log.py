"""
"""
import logging
import logging.config

log_configuration = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": { 
        "standard": {
            "format": "%(asctime)s [%(name)s] %(levelname)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S%z"
        }
    },
    "handlers": { 
        "console": { 
            "level": "DEBUG",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout"
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}


def init(level):
    logging.config.dictConfig(log_configuration)
    logging.getLogger().setLevel(level)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
