
import os
import sys
import pytest
# change dir to backend folder
# Add the backend directory to Python's import path
test_path = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
common_path = os.path.join(os.path.dirname(backend_path), "common")
os.chdir(backend_path) # change to 2 levels up (backend folder)
sys.path.insert(0, common_path)
sys.path.insert(0, backend_path)

from main_db import db_connect
from config import filly_trkr_config
