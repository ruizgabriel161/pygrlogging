import json
from pathlib import Path


class TemplateJson:
    """
    Classe responsavel por criar o arquivo json de configuração do lig
    """

    def __init__(self) -> None:

        self.log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "file": {
                    "class": "logging.Formatter",
                    "format": "FILE: [%(created)f|%(name)s|%(filename)s|"
                            "%(lineno)d|%(levelname)s|%(message)s]",
                },
                "json": {
                    "()": "pygrlogging.formatters.JSONLogFormatter",
                    "include_keys": [
                        "created",
                        "filename",
                        "name",
                        "levelname",
                        "lineno",
                        "message",
                    ],
                    "datefmt": "%d/%m/%Y %H:%M:%S",
                },
                "console_stdout": {
                    "class": "logging.Formatter",
                    "format": "%(created)f|%(filename)s|%(name)s|%(levelname)s"
                            "|%(lineno)d|%(message)s",
                    "datefmt": "[%X]",
                },
                "console_stderr": {
                    "class": "logging.Formatter",
                    "format": "%(created)f|%(filename)s|%(name)s|"
                            "%(levelname)s|%(lineno)d|%(message)s",
                    "datefmt": "[%X]",
                },
            },
            "filters": {
                "max_level_info": {
                    "()": "pygrlogging.filters.MaxLevelFilter",
                    "max_level": "INFO",
                },
            },
            "handlers": {
                "queue": {
                    "class": "logging.handlers.QueueHandler",
                    "handlers": [
                        "file",
                        "console_stdout",
                        "console_stderr",
                    ],
                    "respect_handler_level": True,
                },
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": "logs/log.log",
                    "maxBytes": 1024,
                    "backupCount": 3,
                    "encoding": "utf-8",
                    "formatter": "json",
                    "mode": "w",
                },
                "console_stdout": {
                    "()": "pygrlogging.handlers.MyRichHandler",
                    "formatter": "console_stdout",
                    "show_time": True,
                    "show_level": True,
                    "rich_tracebacks": True,
                    "enable_link_path": True,
                    "markup": True,
                    "show_path": True,
                    "omit_repeated_times": False,
                    "file": "stdout",
                    "level": "DEBUG",
                    "filters": [
                        "max_level_info",
                    ],
                },
                "console_stderr": {
                    "()": "pygrlogging.handlers.MyRichHandler",
                    "formatter": "console_stderr",
                    "show_time": True,
                    "show_level": True,
                    "rich_tracebacks": True,
                    "enable_link_path": True,
                    "markup": False,
                    "show_path": True,
                    "omit_repeated_times": False,
                    "file": "stderr",
                    "level": "WARNING",
                },
            },
            "root": {
                "level": "INFO",
                "handlers": [
                    "queue",
                ],
            },
        }


    def dict_to_json(self, path: Path) -> None:
        '''
        dict_to_json Método responsável por transformar o dict em json e salva-lo

        Args:
            path (Path): caminho do arquivo

        Raises:
            FileExistsError: Erro caso o arquivo exista
            RuntimeError: erro ao criar o arquivo
        '''

        file_path = path.resolve()

        if file_path.exists():
            raise FileExistsError(f'File {file_path} already exists!')

        try:
            with file_path.open("w", encoding="utf-8") as f:
                json.dump(self.log_config, f, indent=4, ensure_ascii=False)
        except RuntimeError as e:
            raise RuntimeError(f'Error creating file {e}')
