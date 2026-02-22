import atexit
import json
import logging
from logging.config import dictConfig
from logging.handlers import QueueHandler, QueueListener
from pathlib import Path

from pygrlogging.template_log_config import TemplateJson


class LoggingConfig:
    """
    Classe responsável por abstrair as configurações do logging
    """

    _instance = None
    _initialized: bool = False

    def __new__(cls, *args, **kwargs):
        """
        __new__ Implementação do padrão singleton para evitar multiplas istânciais

        Returns:
            cls: instância da classe
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(
        self,
        config_file: str | Path,
        logs_dir: str | Path
    ):

        if self._initialized:
            return

        self.config_file: Path = Path(config_file).resolve()
        self.logs_dir = Path(logs_dir).resolve()
        self._ensure_config_file()
        self._queue_handler: QueueHandler | None = None
        self._queue_listener: QueueListener | None = None
        self.logger: logging.Logger = logging.getLogger('config_setup')
        self.logger.setLevel(logging.DEBUG)
        self._setup_logging()

        self._initialized = True
         
    def _setup_logging(self) -> None:
        """
        _setup_logging Método responsável a configuração dos logs da aplicação
        """

        try:
            config: dict = self._load_config()

            # Carrega as configuração dos json para o log
            dictConfig(config=config)

            self._queue_handler = self._get_queue_handler()

            self._setup_queue_listener()
            self.logger.debug('Logging configurado com sucesso')

        except Exception as e:
            self.logger.error(f'Erro ao configurar logging: {e}')
            raise

    def _setup_queue_listener(self) -> None:
        if self._queue_handler is not None:
            self._queue_listener = self._queue_handler.listener
            if self._queue_listener is not None:
                # caso exista um handler queue inicia o listener
                self._queue_listener.start()
                atexit.register(self._stop_queue_listener)

    def _stop_queue_listener(self) -> None:
        if self._queue_listener is not None:
            self._queue_listener.stop()

    def _get_queue_handler(self) -> QueueHandler | None:

        queue_handlers = [
            handler
            for handler in logging.getLogger().handlers
            if isinstance(handler, QueueHandler)
        ]

        if len(queue_handlers) > 1:
            msg = 'Não é permitido mais de um QueueHandler'
            self.logger.exception(msg=msg)
            raise RuntimeError(msg)

        if len(queue_handlers) == 1:
            return queue_handlers[0]
        return None

    def _ensure_config_file(self) -> None:
        '''
        _ensure_config_file Metodo responsável criar o template

        Args:
            create_config_file (bool): _description_
        '''
        if not self.config_file.exists():
            template_log_config = TemplateJson()
            template_log_config.dict_to_json(self.config_file)
            return

    def _load_config(self) -> dict:
        """
        _load_config Método para ler o json de configuração

        Returns:
            dict: retorna o json em dicionário
        """
        with self.config_file.open('r', encoding='utf8') as file:
            return json.load(file)

    def get_logger(self, name: str = '') -> logging.Logger:
        """
        Retorna um logger configurado.

        Args:
            name: Nome do logger (geralmente __name__)

        Returns:
            Logger configurado
        """
        return logging.getLogger(name)
