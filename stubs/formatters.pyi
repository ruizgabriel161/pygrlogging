import logging
from _typeshed import Incomplete
from zoneinfo import ZoneInfo as ZoneInfo

LOG_RECORD_KEYS: Incomplete

class JSONLogFormatter(logging.Formatter):
    include_keys: Incomplete
    datefmt: Incomplete
    def __init__(self, include_keys: Union[list[str], None] = ..., datefmt: str = ...) -> None: ...
    def format(self, record: logging.LogRecord) -> str: ...
    def formatTime(self, record: logging.LogRecord, datefmt: Union[str, None] = ...) -> str: ...
