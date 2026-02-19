from pathlib import Path
from typing import Literal, TypeAlias

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LogLevel: TypeAlias = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

class SettingsLooging(BaseSettings):
    model_config: SettingsConfigDict = SettingsConfigDict(
    env_file='.env',  # determina onde está armazena as variaveis de ambiente, 
    extra='ignore', # permite variáveis desconhecidas,
    case_sensitive=True
    )

    ROOT_DIR: Path = Path(".").resolve()
    LOGS_DIR: Path = Path("logs")
    LOGGING_CONFIG_JSON: Path = Path("logging.json")

    # -------------------------
    # Logger config
    # -------------------------

    SETUP_LOGGER_NAME: str = "setup"
    SETUP_LOGGER_LEVEL: LogLevel = "WARNING"
    DEFAULT_LOGGER_LEVEL: LogLevel = "WARNING"

    @field_validator('LOGS_DIR')
    @classmethod
    def validate_logs_dir(cls, path: Path | str) -> Path:
        '''
        validate_logs_dir Método responsável por verificar e garantir a existência de uma página de logs

        Args:
            path (Path | str): caminho do arquivo

        Returns:
            Path: caminho da pasta de logs
        '''        
        if isinstance(path, str):
            path = Path(path).resolve()
        
        if not path.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        return path

    @field_validator('LOGGING_CONFIG_JSON')
    @classmethod
    def validate_logs_file(cls, path: Path) -> Path:
        '''
        validate_logs_file Método responsável por verificar a existência do arquivo de configuração

        Args:
            path (Path): Caminho do arquivo

        Raises:
            FileNotFoundError: Caso o arquivo não for encontrado

        Returns:
            Path: retorna o caminho
        '''        

        if isinstance(path, str):
            path = Path(path).resolve()
        if not path.is_file():
             raise FileNotFoundError(path)
        return path

    @field_validator('DEFAULT_LOGGER_LEVEL')
    @classmethod
    def validate_level(cls, level: str) -> LogLevel:
        '''
        validate_level Método responsável por verificar o level do log

        Args:
            level (str): level padrão do log

        Raises:
            ValueError: erro caso o level não exista    

        Returns:
            LogLevel: retorna o level padrão
        '''        
        level = level.upper()
        if level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
             msg = 'Level escolhido não suportado pelo Logging'
             raise ValueError(msg)
        return level #pyright: ignore
    