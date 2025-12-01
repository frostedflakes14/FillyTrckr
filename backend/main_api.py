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

    def __init__(self, config=filly_trkr_config()):
        """Initialize the FastAPI application."""
        self._config = config
        self.app = FastAPI(title="Filly Trckr API", version="1.0.0")
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

        @self.app.get(
                "/api/v1/filly/brands",
                response_model=api_models.response_get_brands,
                summary="Get all filly brands",
                description="Retrieve a list of all filament brands in the database.",
                tags=["Get Roll Properties"],
                )
        async def get_brands():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            brands = self.db.get_filly_brands()
            return {"brands": brands}

        @self.app.get(
                "/api/v1/filly/types",
                response_model=api_models.response_get_types,
                summary="Get all filly types",
                description="Retrieve a list of all filament types in the database.",
                tags=["Get Roll Properties"],
                )
        async def get_types():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            types = self.db.get_filly_types()
            return {"types": types}

        @self.app.get(
                "/api/v1/filly/colors",
                response_model=api_models.response_get_colors,
                summary="Get all filly colors",
                description="Retrieve a list of all filament colors in the database.",
                tags=["Get Roll Properties"],
                )
        async def get_colors():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            colors = self.db.get_filly_colors()
            return {"colors": colors}

        @self.app.get(
                "/api/v1/filly/subtypes",
                response_model=api_models.response_get_subtypes,
                summary="Get all filly subtypes",
                description="Retrieve a list of all filament subtypes in the database.",
                tags=["Get Roll Properties"],
                )
        async def get_subtypes():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            subtypes = self.db.get_filly_subtypes()
            return {"subtypes": subtypes}

        @self.app.get(
                "/api/v1/filly/rolls/all",
                response_model=api_models.response_get_rolls,
                summary="Get all filly rolls",
                description="Retrieve a list of all filament rolls in the database.",
                tags=["Get Rolls"],
                )
        async def get_all_rolls():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            rolls = self.db.get_filly_rolls_all()
            return {"rolls": rolls}

        @self.app.get(
                "/api/v1/filly/rolls/active",
                response_model=api_models.response_get_rolls,
                summary="Get active (weight>0) filly rolls",
                description="Retrieve a list of all active filament rolls in the database.",
                tags=["Get Rolls"],
                )
        async def get_active_rolls():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            rolls = self.db.get_filly_rolls_active()
            return {"rolls": rolls}

        @self.app.get(
                "/api/v1/filly/rolls/in_use",
                response_model=api_models.response_get_rolls,
                summary="Get in-use (on printer) filly rolls",
                description="Retrieve a list of all in-use filament rolls in the database.",
                tags=["Get Rolls"],
                )
        async def get_in_use_rolls():
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")
            rolls = self.db.get_filly_rolls_in_use()
            return {"rolls": rolls}

        # POST endpoints to update roll status

        @self.app.post(
                "/api/v1/filly/rolls/{roll_id}/set_in_use",
                response_model=api_models.response_roll_update,
                summary="Set roll in-use status",
                description="Set the in-use status of a specific roll to True or False.",
                tags=["Update Rolls"],
                )
        async def roll_set_in_use(roll_id: int, data: api_models.request_roll_set_in_use):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            result = self.db.change_in_use_status(roll_id, data.in_use)
            if not result.get('result', False):
                raise HTTPException(status_code=404, detail="Roll not found or could not update") # TODO consider having the db function return the error message
            return result

        @self.app.post(
                "/api/v1/filly/rolls/{roll_id}/duplicate",
                response_model=api_models.response_roll_update,
                summary="Duplicate a roll",
                description="Create a duplicate of a specific roll. Optionally, set a new original weight.",
                tags=["Create Rolls"],
                )
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

        @self.app.post(
                "/api/v1/filly/rolls/{roll_id}/set_opened",
                response_model=api_models.response_roll_update,
                summary="Set a roll as opened",
                description="Set the opened status of a specific roll to True. Not capable of setting it to False.",
                tags=["Update Rolls"],
                )
        async def roll_set_opened(roll_id: int):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            result = self.db.open_roll(roll_id)
            if not result.get('result', False):
                raise HTTPException(status_code=404, detail="Roll not found or could not update")
            return result

        @self.app.post(
                "/api/v1/filly/rolls/{roll_id}/update_weight",
                response_model=api_models.response_roll_update,
                summary="Update the weight of a roll",
                description="Update the weight of a specific roll by setting a new weight or decreasing the current weight.",
                tags=["Update Rolls"],
                )
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

        @self.app.post(
                "/api/v1/filly/rolls/add",
                response_model=api_models.response_roll_update,
                summary="Add a new roll",
                description="Requires all fields for a new roll, and adds it to the database.",
                tags=["Create Rolls"],
                )
        async def roll_add(data: api_models.request_roll_add):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            required_items = [data.type_id, data.brand_id, data.color_id, data.subtype_id, data.original_weight_grams]
            if not all(item is not None for item in required_items):
                raise HTTPException(status_code=400, detail="Missing required fields to add roll")

            # TODO clean the inputs
            result = self.db.insert_roll(
                type_id=data.type_id,
                brand_id=data.brand_id,
                color_id=data.color_id,
                subtype_id=data.subtype_id,
                original_weight_grams=data.original_weight_grams,
                weight_grams=data.get('weight_grams', None),
                opened=data.get('opened', False),
                in_use=data.get('in_use', False),
            )
            if not result.get('result', False):
                raise HTTPException(status_code=400, detail="Failed to add roll")
            return result

        # TODO api endpoints to make: get rolls-filtered

    def run(self, host=None, port=None):
        """Run the FastAPI application.

        Args:
            host (str): Host to bind to. Defaults to "0.0.0.0" (from config)
            port (int): Port to bind to. Defaults to 8000 (from config)
        """
        if host is None:
            host = self._config.api_info.host
        if port is None:
            port = self._config.api_info.port
        uvicorn.run(self.app, host=host, port=port)


def main():
    """Main entry point to run the FastAPI application standalone."""
    api = FillyAPI()
    logger.warning("Running API without database connection. Some endpoints will fail.")
    api.run()


if __name__ == "__main__":
    main()