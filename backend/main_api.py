from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn
import sys
from pathlib import Path
import api_models as api_models

common_path = Path(__file__).parent.parent / "common"
sys.path.insert(0, str(common_path))
from config import filly_trkr_config
from common_logging import get_logger

logger = get_logger(__name__)


class FillyAPI:
    """FastAPI application wrapper for Filly Tracker.

    Manages the FastAPI instance and database connection.
    """

    def __init__(self):
        """Initialize the FastAPI application."""
        self.app = FastAPI(title="Filly Tracker API", version="1.0.0")
        self.db = None

        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Register routes
        self._register_routes()

    def connect_to_db(self, db_connection):
        """Connect the API to a database instance.

        Args:
            db_connection: A db_connect instance from main_db.py
        """
        self.db = db_connection
        logger.info("API connected to database successfully.")

    def _register_routes(self):
        """Register all API routes."""

        # @self.app.get("/api/v1/filly/get_version")
        # async def get_version():
        #     return {"version": "1.0.0"}

        @self.app.get("/api/v1/filly/brands", response_model=api_models.response_get_brands)
        async def get_brands():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            brands = self.db.get_filly_brands()
            return {"brands": brands}

        @self.app.get("/api/v1/filly/types", response_model=api_models.response_get_types)
        async def get_types():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            types = self.db.get_filly_types()
            return {"types": types}

        @self.app.get("/api/v1/filly/colors", response_model=api_models.response_get_colors)
        async def get_colors():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            colors = self.db.get_filly_colors()
            return {"colors": colors}

        @self.app.get("/api/v1/filly/subtypes", response_model=api_models.response_get_subtypes)
        async def get_subtypes():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            subtypes = self.db.get_filly_subtypes()
            return {"subtypes": subtypes}

        @self.app.get("/api/v1/filly/rolls/all", response_model=api_models.response_get_rolls)
        async def get_all_rolls():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            rolls = self.db.get_filly_rolls_all()
            return {"rolls": rolls}

        @self.app.get("/api/v1/filly/rolls/active", response_model=api_models.response_get_rolls)
        async def get_active_rolls():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            rolls = self.db.get_filly_rolls_active()
            return {"rolls": rolls}

        @self.app.get("/api/v1/filly/rolls/in_use", response_model=api_models.response_get_rolls)
        async def get_in_use_rolls():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            rolls = self.db.get_filly_rolls_in_use()
            return {"rolls": rolls}

        # POST endpoints to update roll status

        @self.app.post("/api/v1/filly/rolls/{roll_id}/set_in_use", response_model=api_models.response_roll_update)
        async def roll_set_in_use(roll_id: int, data: api_models.request_roll_set_in_use):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            result = self.db.change_in_use_status(roll_id, data.in_use)
            if not result.get('result', False):
                raise HTTPException(status_code=404, detail="Roll not found or could not update") # TODO consider having the db function return the error message
            return result

        @self.app.post("/api/v1/filly/rolls/{roll_id}/duplicate", response_model=api_models.response_roll_update)
        async def roll_duplicate(roll_id: int, data: Optional[api_models.request_roll_duplicate] = None):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            if data and data.original_weight_grams is not None:
                result = self.db.insert_dup_roll(roll_id, original_weight_grams=data.original_weight_grams)
            else:
                result = self.db.insert_dup_roll(roll_id)
            if not result.get('result', False):
                raise HTTPException(status_code=404, detail="Roll not found or could not duplicate")
            return result

        @self.app.post("/api/v1/filly/rolls/{roll_id}/set_opened", response_model=api_models.response_roll_update)
        async def roll_set_opened(roll_id: int):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            result = self.db.open_roll(roll_id)
            if not result.get('result', False):
                raise HTTPException(status_code=404, detail="Roll not found or could not update")
            return result

        @self.app.post("/api/v1/filly/rolls/{roll_id}/update_weight", response_model=api_models.response_roll_update)
        async def roll_update_weight(roll_id: int, data: api_models.request_roll_update_weight):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            # Update roll weight can be set or can be decreased depending on what is in data
            if data.new_weight_grams is not None:
                result = self.db.update_roll_weight(roll_id, new_weight_grams=data.new_weight_grams)
            elif data.decrease_by_grams is not None:
                result = self.db.update_roll_weight(roll_id, decr_weight_grams=data.decrease_by_grams)
            else:
                raise HTTPException(status_code=400, detail="No weight update data provided")

            if not result.get('result', False):
                raise HTTPException(status_code=404, detail="Roll not found or could not update")
            return result

        # TODO api endpoints to make: insert_roll, get rolls-filtered

    def run(self, host="0.0.0.0", port=8000):
        """Run the FastAPI application.

        Args:
            host (str): Host to bind to. Defaults to "0.0.0.0".
            port (int): Port to bind to. Defaults to 8000.
        """
        uvicorn.run(self.app, host=host, port=port)


def main():
    """Main entry point to run the FastAPI application standalone."""
    api = FillyAPI()
    logger.warning("Running API without database connection. Some endpoints will fail.")
    api.run()


if __name__ == "__main__":
    main()