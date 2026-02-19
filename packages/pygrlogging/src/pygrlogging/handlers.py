
from logging import LogRecord
from logging.handlers import QueueHandler
import sys
from typing import Any, Literal

from rich.console import Console
from rich.logging import RichHandler


class MyRichHandler(RichHandler):
    def __init__(self, file: Literal['stdout', 'stderr'], **kwargs: Any) -> None:
        super().__init__(**kwargs)

        if file not in ['stdout', 'stderr']:
            ValueError('file in not stdout or stderr')

        console = Console(file=getattr(sys,file))
        self.console = console
