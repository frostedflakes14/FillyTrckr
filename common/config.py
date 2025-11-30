import json
import os
from common_logging import get_logger

logger = get_logger()

class filly_trkr_config:
    """Configuration class for FillyTrckr application.

    Loads settings from a JSON configuration file, or from environment variables if needed.
    """

    class DatabaseInfo():
        def __init__(self, d, config_filepath):
            self._d = d
            self._config_filepath = config_filepath

        @property
        def type(self):
            return self._d.get("type", "sqlite")

        @property
        def host(self):
            return self._d.get("host", "localhost")

        @property
        def port(self):
            return self._d.get("port", "5432")

        @property
        def username(self):
            return self._d.get("username")

        @property
        def password(self):
            return self._d.get("password")

        @property
        def db_name(self):
            if self.type == 'sqlite':
                return self._d.get('db_name', 'example.db')
            else:
                return self._d.get('db_name', 'mydatabase')

        @property
        def db_dir(self):
            if self.type == 'sqlite':
                # use relative path from config file location
                db_dir = self._d.get('db_dir', '.')
                if not os.path.isabs(db_dir):
                    db_dir = os.path.join(os.path.dirname(self._config_filepath), db_dir)
                return db_dir
            else:
                return None

        @property
        def _db_connection_string(self):
            if self.type == 'sqlite':
                return f'sqlite:///{self.db_dir}/{self.db_name}'
            elif self.type in ['postgres', 'postgresql']:
                return f'postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}'
            else:
                raise ValueError(f"Unsupported database type: {self.type}")

    def __init__(self, config_filepath=None):
        self._config = self._load_config(config_filepath)
        if config_filepath is None:
            config_filepath = __file__
        else:
            self._config_filepath = config_filepath

    def _load_config(self, config_filepath):
        config = {}
        if config_filepath is None:
            # by default, it looks for it in the same directory as this file
            config_filepath = os.path.join(os.path.dirname(__file__), "config.json")

        if os.path.exists(config_filepath):
            try:
                logger.info(f'Found config file at {config_filepath}, loading settings.')
                with open(config_filepath, 'r') as f:
                    config = json.load(f)
                return config
            except json.JSONDecodeError:
                logger.error("config.json is not a valid JSON file.")
                raise
            except Exception as e:
                logger.error(f"An unexpected error occurred while loading config.json: {e}")
                raise
        else:
            logger.info(f'Config file not found at {config_filepath}, loading environment variables.')
            return self._load_env_vars()

    def _load_env_vars(self):
        config = {}
        config["TZ"] = os.getenv("TZ", "America/Detroit")
        config["database_info"] = {
            "type": os.getenv("DB_TYPE", "sqlite"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": int(os.getenv("DB_PORT", 5432)),
            "username": os.getenv("DB_USERNAME", "user"),
            "password": os.getenv("DB_PASSWORD", "password"),
            "db_name": os.getenv("DB_NAME", "example.db"),
            "db_dir": os.getenv("DB_DIR", os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db')),
        }
        return config

    @property
    def TZ(self):
        return self._config.get("TZ", "America/Detroit")

    @property
    def database_info(self):
        return self.DatabaseInfo(self._config.get("database_info", {}), self._config_filepath)

