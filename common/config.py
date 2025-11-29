import json
import os

class filly_trkr_config:
    """Configuration class for FillyTrckr application.

    Loads settings from a JSON configuration file, or from environment variables if needed.
    """

    class DatabaseInfo():
        def __init__(self, d):
            self._d = d

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
                return self._d.get('db_dir', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db'))
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

    def __init__(self):
        self._config = self._load_config()

    def _load_config(self, config_filepath=None):
        config = {}
        if config_filepath is None:
            config_filepath = os.path.join(os.path.dirname(__file__), "config.json")

        if os.path.exists(config_filepath):
            try:
                print(f'Found config file at {config_filepath}, loading settings.')
                with open(config_filepath, 'r') as f:
                    config = json.load(f)
                return config
            except json.JSONDecodeError:
                print("config.json is not a valid JSON file.")
                raise
            except Exception as e:
                print(f"An unexpected error occurred while loading config.json: {e}")
                raise
        else:
            print(f'Config file not found at {config_filepath}, loading environment variables.')
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
        return self.DatabaseInfo(self._config.get("database_info", {}))

