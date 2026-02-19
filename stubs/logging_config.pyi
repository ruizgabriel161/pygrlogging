import logging
from _typeshed import Incomplete
from pathlib import Path

class LoggingConfig:
    def __new__(cls, *args, **kwargs): ...
    config_file: Incomplete
    logs_dir: Incomplete
    logger: Incomplete
    def __init__(self, config_file: Union[str, Path], logs_dir: Union[str, Path]) -> None: ...
    def get_logger(self, name: str = ...) -> logging.Logger: ...
