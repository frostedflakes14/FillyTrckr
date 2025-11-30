
import os
import sys
import pytest
# change dir to common folder
os.chdir(os.path.dirname(os.path.dirname(__file__))) # change to 2 levels up (backend folder)
# Add the common directory to Python's import path
test_path = os.path.dirname(os.path.abspath(__file__))
common_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, common_path)

from config import filly_trkr_config

@pytest.fixture
def config_sqlite():
    config = filly_trkr_config(os.path.join(test_path, "test_config_1.json"))
    return config

@pytest.fixture
def config_postgres():
    config = filly_trkr_config(os.path.join(test_path, "test_config_2.json"))
    return config

def test_database_info_sqlite(config_sqlite):
    db_info = config_sqlite.database_info
    assert db_info.type == "sqlite"
    assert db_info.db_name == "test_sqlite.db"
    assert db_info.db_dir == os.path.join(test_path, ".")
    assert db_info._db_connection_string == f"sqlite:///{os.path.join(test_path, '.')}/test_sqlite.db"

def test_database_info_postgres(config_postgres):
    db_info = config_postgres.database_info
    assert db_info.type == "postgres"
    assert db_info.host == "localhost"
    assert db_info.port == "5432"
    assert db_info.username == "testuser"
    assert db_info.password == "testpass"
    assert db_info.db_name == "testdb"
    assert db_info._db_connection_string == "postgresql://testuser:testpass@localhost:5432/testdb"