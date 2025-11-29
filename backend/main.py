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
from main_db import db_connect
from main_api import FillyAPI

logger = get_logger(__name__)


def main():
    """Initialize and run the Filly Tracker application."""
    logger.info("Starting Filly Tracker application...")

    # Initialize database connection
    logger.info("Initializing database...")
    db = db_connect()

    if not db.db_connected:
        logger.error("Failed to connect to database. Exiting.")
        sys.exit(1)

    # Initialize API
    logger.info("Initializing API...")
    api = FillyAPI()

    # Connect API to database
    api.connect_to_db(db)

    # Start the server
    logger.info("Starting API server on http://0.0.0.0:8000")
    api.run(host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
