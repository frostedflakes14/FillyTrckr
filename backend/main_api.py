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

    def __init__(self, config=filly_trkr_config(), db_connection=None):
        """Initialize the FastAPI application."""
        self._config = config

        # Define tag metadata with order and descriptions
        tags_metadata = [
            {
                "name": "Get Rolls",
                "description": "Retrieve filament rolls with various filters and criteria.",
            },
            {
                "name": "Create Rolls",
                "description": "Add new rolls or duplicate existing ones.",
            },
            {
                "name": "Update Rolls",
                "description": "Modify existing roll properties such as weight, status, and usage.",
            },
            {
                "name": "Roll Properties",
                "description": "Retrieve available brands, types, colors, and subtypes for filament rolls.",
            },
        ]

        self.app = FastAPI(
            title="FillyTrckr API",
            version="1.0.0",
            openapi_tags=tags_metadata,
            docs_url = "/api-docs"
        )
        self.db = None

        # Configure CORS
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        logger.info("Initializing API...")
        # Register routes
        self._register_routes()

        if db_connection is not None:
            self.connect_to_db(db_connection)

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

        # Add health check endpoint
        @self.app.get(
                "/api/health",
                summary="Health check",
                description="Check the health status of the API.",
                tags=["Health Check"],
                )
        async def health_check():
            if not self.db:
                return {"status": "unhealthy", "detail": "Database not connected"}
            else:
                return {"status": "healthy"}

        @self.app.get(
                "/api/v1/filly/brands",
                response_model=api_models.response_get_brands,
                summary="Get all filly brands",
                description="Retrieve a list of all filament brands in the database.",
                tags=["Roll Properties"],
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
                tags=["Roll Properties"],
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
                tags=["Roll Properties"],
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
                tags=["Roll Properties"],
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
                "/api/v1/filly/colors/add",
                response_model=api_models.response_color_add,
                summary="Add a new filly color",
                description="Add a new filament color to the database.",
                tags=["Roll Properties"],
                )
        async def add_color(data: api_models.request_color_add):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            if not data.name or not data.name.strip():
                raise HTTPException(status_code=400, detail="Color name cannot be empty")

            if not data.hex_code or not data.hex_code.strip():
                raise HTTPException(status_code=400, detail="Color hex code cannot be empty")

            result = self.db.insert_filly_color(color_name=data.name.strip().lower(), hex_code=data.hex_code.strip())
            if not result.get('result', False):
                raise HTTPException(status_code=400, detail="Failed to add color")
            return result['color']

        @self.app.post(
                "/api/v1/filly/types/add",
                response_model=api_models.response_type_add,
                summary="Add a new filly type",
                description="Add a new filament type to the database.",
                tags=["Roll Properties"],
                )
        async def add_type(data: api_models.request_type_add):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            if not data.name or not data.name.strip():
                raise HTTPException(status_code=400, detail="Type name cannot be empty")

            result = self.db.insert_filly_type(type_name=data.name.strip().lower())
            if not result.get('result', False):
                raise HTTPException(status_code=400, detail="Failed to add type")
            return result['type']

        @self.app.post(
                "/api/v1/filly/subtypes/add",
                response_model=api_models.response_subtype_add,
                summary="Add a new filly subtype",
                description="Add a new filament subtype to the database.",
                tags=["Roll Properties"],
                )
        async def add_subtype(data: api_models.request_subtype_add):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            if not data.name or not data.name.strip():
                raise HTTPException(status_code=400, detail="Subtype name cannot be empty")

            result = self.db.insert_filly_subtype(subtype_name=data.name.strip().lower())
            if not result.get('result', False):
                raise HTTPException(status_code=400, detail="Failed to add subtype")
            return result['subtype']

        @self.app.post(
                "/api/v1/filly/brands/add",
                response_model=api_models.response_brand_add,
                summary="Add a new filly brand",
                description="Add a new filament brand to the database.",
                tags=["Roll Properties"],
                )
        async def add_brand(data: api_models.request_brand_add):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            if not data.name or not data.name.strip():
                raise HTTPException(status_code=400, detail="Brand name cannot be empty")

            result = self.db.insert_filly_brand(brand_name=data.name.strip().lower())
            if not result.get('result', False):
                raise HTTPException(status_code=400, detail="Failed to add brand")
            return result['brand']

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

        # Helper function for filter logic
        def _get_filtered_rolls_logic(
                data: Optional[api_models.request_roll_filter] = None,
                brand_id: Optional[int] = None,
                type_id: Optional[int] = None,
                color_id: Optional[int] = None,
                subtype_id: Optional[int] = None,
                opened: Optional[bool] = None,
                in_use: Optional[bool] = None,
            ):
            if not self.db:
                raise HTTPException(status_code=500, detail="Database not connected")

            # Start with query parameters, then override with JSON body values if provided
            filters = {
                "brand_id": brand_id,
                "type_id": type_id,
                "color_id": color_id,
                "subtype_id": subtype_id,
                "opened": opened,
                "in_use": in_use,
            }

            # Override with JSON body values if provided
            if data:
                if data.brand_id is not None:
                    filters["brand_id"] = data.brand_id
                if data.type_id is not None:
                    filters["type_id"] = data.type_id
                if data.color_id is not None:
                    filters["color_id"] = data.color_id
                if data.subtype_id is not None:
                    filters["subtype_id"] = data.subtype_id
                if data.opened is not None:
                    filters["opened"] = data.opened
                if data.in_use is not None:
                    filters["in_use"] = data.in_use

            # clean the inputs, set all text to lowercase (or None), a validate ints/bools as needed
            if filters["brand_id"] is not None:
                try:
                    filters["brand_id"] = int(filters["brand_id"])
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid brand_id value")
            if filters["type_id"] is not None:
                try:
                    filters["type_id"] = int(filters["type_id"])
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid type_id value")
            if filters["color_id"] is not None:
                try:
                    filters["color_id"] = int(filters["color_id"])
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid color_id value")
            if filters["subtype_id"] is not None:
                try:
                    filters["subtype_id"] = int(filters["subtype_id"])
                except ValueError:
                    raise HTTPException(status_code=400, detail="Invalid subtype_id value")
            if filters["opened"] is not None:
                if isinstance(filters["opened"], str):
                    if filters["opened"].lower() in ['true', '1', 'yes']:
                        filters["opened"] = True
                    elif filters["opened"].lower() in ['false', '0', 'no']:
                        filters["opened"] = False
                    else:
                        raise HTTPException(status_code=400, detail="Invalid opened value")
            if filters["in_use"] is not None:
                if isinstance(filters["in_use"], str):
                    if filters["in_use"].lower() in ['true', '1', 'yes']:
                        filters["in_use"] = True
                    elif filters["in_use"].lower() in ['false', '0', 'no']:
                        filters["in_use"] = False
                    else:
                        raise HTTPException(status_code=400, detail="Invalid in_use value")

            rolls = self.db.get_filly_rolls_active_filter(
                type_id=filters["type_id"],
                brand_id=filters["brand_id"],
                color_id=filters["color_id"],
                subtype_id=filters["subtype_id"],
                opened=filters["opened"],
                in_use=filters["in_use"],
            )
            return {"rolls": rolls}

        @self.app.get(
                "/api/v1/filly/rolls/filter",
                response_model=api_models.response_get_rolls,
                summary="Get active filly rolls with filters (GET)",
                description="Retrieve a list of filament rolls in the database based on provided filters via query parameters.",
                tags=["Get Rolls"],
                )
        async def get_filtered_rolls_get(
                brand_id: Optional[int] = None,
                type_id: Optional[int] = None,
                color_id: Optional[int] = None,
                subtype_id: Optional[int] = None,
                opened: Optional[bool] = None,
                in_use: Optional[bool] = None,
            ):
            return _get_filtered_rolls_logic(
                None, brand_id, type_id, color_id, subtype_id, opened, in_use
            )

        @self.app.post(
                "/api/v1/filly/rolls/filter",
                response_model=api_models.response_get_rolls,
                summary="Get active filly rolls with filters (POST)",
                description="Retrieve a list of filament rolls in the database based on provided filters. Accepts filters from both query parameters and JSON body. JSON body values take precedence over query parameters.",
                tags=["Get Rolls"],
                )
        async def get_filtered_rolls_post(
                data: Optional[api_models.request_roll_filter] = None,
                brand_id: Optional[int] = None,
                type_id: Optional[int] = None,
                color_id: Optional[int] = None,
                subtype_id: Optional[int] = None,
                opened: Optional[bool] = None,
                in_use: Optional[bool] = None,
            ):
            return _get_filtered_rolls_logic(
                data, brand_id, type_id, color_id, subtype_id, opened, in_use
            )

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
        logger.info(f"Starting API server on http://{host}:{port}")
        uvicorn.run(self.app, host=host, port=port)


def main():
    """Main entry point to run the FastAPI application standalone."""
    api = FillyAPI()
    logger.warning("Running API without database connection. Some endpoints will fail.")
    api.run()


if __name__ == "__main__":
    main()