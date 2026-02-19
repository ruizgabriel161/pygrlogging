from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import TypeAlias

LogLevel: TypeAlias

class SettingsLooging(BaseSettings):
    model_config: SettingsConfigDict
    ROOT_DIR: Path
    LOGS_DIR: Path
    LOGGING_CONFIG_JSON: Path
    SETUP_LOGGER_NAME: str
    SETUP_LOGGER_LEVEL: LogLevel
    DEFAULT_LOGGER_LEVEL: LogLevel
    @classmethod
    def validate_logs_dir(cls, path: Union[Path, str]) -> Path: ...
    @classmethod
    def validate_logs_file(cls, path: Path) -> Path: ...
    @classmethod
    def validate_level(cls, level: str) -> LogLevel: ...
