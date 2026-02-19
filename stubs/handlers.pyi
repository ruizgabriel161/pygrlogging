from _typeshed import Incomplete
from logging import LogRecord as LogRecord
from logging.handlers import QueueHandler as QueueHandler
from rich.logging import RichHandler
from typing import Any, Literal

class MyRichHandler(RichHandler):
    console: Incomplete
    def __init__(self, file: Literal['stdout', 'stderr'], **kwargs: Any) -> None: ...
