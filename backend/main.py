"""Main entry point for the Filly Tracker application.

Initializes the database connection and FastAPI application,
then starts the API server.
"""

import sys
from pathlib import Path

# Add common directory to path for imports
common_path = Path(__file__).parent.parent / "common"
sys.path.insert(0, str(common_path))

from common_logging import get_logger
from config import filly_trkr_config
from main_db import db_connect
from main_api import FillyAPI

logger = get_logger(__name__)

def main():
    """Initialize and run the Filly Tracker application."""
    logger.info("Starting Filly Tracker application...")

    config = filly_trkr_config()

    # Initialize database connection
    db = db_connect(config=config)
    if not db.db_connected:
        logger.error("Failed to connect to database. Exiting.")
        sys.exit(1)

    # Initialize API
    api = FillyAPI(config=config, db_connection=db)
    # Start the server
    api.run()


if __name__ == "__main__":
    main()
