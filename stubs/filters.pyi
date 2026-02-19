import logging
from _typeshed import Incomplete

class MaxLevelFilter(logging.Filter):
    max_level: Incomplete
    def __init__(self, max_level: str) -> None: ...
    def filter(self, record: logging.LogRecord) -> bool: ...
