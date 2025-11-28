"""Database configuration and initialization module.

Supports both SQLite (for development) and PostgreSQL (for production).
Database type and credentials are configurable via environment variables.

Provides a DatabaseConnection class for managing all database operations.
"""

import os
import sys
from pathlib import Path
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import OperationalError

# Add common directory to path for imports
common_path = Path(__file__).parent.parent / "common"
sys.path.insert(0, str(common_path))

from db_base import Base
from db_classes import (
    db_filly_types,
    db_filly_brands,
    db_filly_surfaces,
    db_filly_colors,
    db_filly_subtypes,
    db_filly_roll
)
from populate_default_tables import (
    filly_types_defaults,
    filly_brands_defaults,
    filly_surfaces_defaults,
    filly_colors_defaults,
    filly_subtypes_defaults
)


# Load configuration from environment variables
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fillytrckr")

# SQLite database path
SQLITE_DB_PATH = Path(__file__).parent.parent / "example.db"


class db_connect:
    """Database connection manager class.

    Handles database initialization, connection management, and provides
    methods for querying and inserting data.
    """

    def __init__(self):
        """Initialize the database connection.

        Creates the engine, initializes schema if needed, and populates
        default data. Does not maintain an open session.
        """
        self.engine = None
        self.SessionLocal = None
        self._initialize_database()

    def _initialize_database(self):
        """Internal method to set up the database engine and schema."""
        if DB_TYPE == "sqlite":
            # SQLite configuration
            db_url = f"sqlite:///{SQLITE_DB_PATH}"
            print(f"Using SQLite database at: {SQLITE_DB_PATH}")
            self.engine = create_engine(db_url, echo=False)

            # Check if database exists, if not create it
            if not SQLITE_DB_PATH.exists():
                print("Database does not exist. Creating new SQLite database...")
                Base.metadata.create_all(self.engine)
                print("Database schema created successfully.")
            else:
                print("Existing SQLite database found.")

        elif DB_TYPE in ["postgres", "postgresql"]:
            # PostgreSQL configuration
            if not DB_USERNAME or not DB_PASSWORD:
                raise ValueError(
                    "PostgreSQL requires DB_USERNAME and DB_PASSWORD environment variables to be set."
                )

            db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            print(f"Attempting to connect to PostgreSQL database at {DB_HOST}:{DB_PORT}/{DB_NAME}")

            try:
                self.engine = create_engine(db_url, echo=False)
                # Test the connection
                with self.engine.connect() as conn:
                    print("Successfully connected to PostgreSQL database.")
            except OperationalError as e:
                raise ConnectionError(
                    f"Failed to connect to PostgreSQL database. Error: {str(e)}"
                ) from e

        else:
            raise ValueError(
                f"Unsupported DB_TYPE: {DB_TYPE}. Supported types are 'sqlite', 'postgres', or 'postgresql'."
            )

        # Create session factory
        self.SessionLocal = sessionmaker(bind=self.engine)

        # Always populate default data (only adds missing entries)
        self._populate_default_data()

    @contextmanager
    def get_session(self):
        """Context manager for database sessions.

        Yields:
            Session: A SQLAlchemy session object

        Example:
            with db.get_session() as session:
                results = session.query(db_filly_types).all()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def _populate_default_data(self):
        """Populate default data into the database tables.

        Only adds entries that don't already exist (checks by name).
        Safe to run multiple times without creating duplicates.
        Uses efficient bulk queries to check existing entries.
        """
        print("Populating default data...")

        with self.get_session() as session:
            added_count = 0

            # Get all existing names in one query per table
            existing_types = {row.name for row in session.query(db_filly_types.name).all()}
            existing_brands = {row.name for row in session.query(db_filly_brands.name).all()}
            existing_surfaces = {row.name for row in session.query(db_filly_surfaces.name).all()}
            existing_colors = {row.name for row in session.query(db_filly_colors.name).all()}
            existing_subtypes = {row.name for row in session.query(db_filly_subtypes.name).all()}

            # Populate filly_types
            for type_name in filly_types_defaults:
                if type_name not in existing_types:
                    session.add(db_filly_types(name=type_name))
                    added_count += 1

            # Populate filly_brands
            for brand_name in filly_brands_defaults:
                if brand_name not in existing_brands:
                    session.add(db_filly_brands(name=brand_name))
                    added_count += 1

            # Populate filly_surfaces
            for surface_name in filly_surfaces_defaults:
                if surface_name not in existing_surfaces:
                    session.add(db_filly_surfaces(name=surface_name))
                    added_count += 1

            # Populate filly_colors
            for color_name in filly_colors_defaults:
                if color_name not in existing_colors:
                    session.add(db_filly_colors(name=color_name))
                    added_count += 1

            # Populate filly_subtypes
            for subtype_name in filly_subtypes_defaults:
                if subtype_name not in existing_subtypes:
                    session.add(db_filly_subtypes(name=subtype_name))
                    added_count += 1

            if added_count > 0:
                print(f"Added {added_count} new default entries.")
            else:
                print("All default data already exists. No new entries added.")

    # TODO create insert and query methods

    def get_filly_rolls_in_use(self):
        """Get all in use filament rolls (on the printer)

        Returns:
            list of dicts of each filly roll, dict defined by to_dict in db_filly_roll class
        """
        with self.get_session() as session:
            rolls = session.query(db_filly_roll).filter_by(in_use=True).all()
            return [roll.to_dict() for roll in rolls]

    def get_filly_rolls_all(self):
        """Get all filament rolls in the database.

        Returns:
            list of dicts of each filly roll, dict defined by to_dict in db_filly_roll class
        """
        with self.get_session() as session:
            rolls = session.query(db_filly_roll).all()
            return [roll.to_dict() for roll in rolls]

    def get_filly_rolls_active(self):
        """Get all active filament rolls (not empty)
        Returns:
            list of dicts of each filly roll, dict defined by to_dict in db_filly_roll class
        """
        with self.get_session() as session:
            rolls = session.query(db_filly_roll).filter(db_filly_roll.weight_grams > 0).all()
            return [roll.to_dict() for roll in rolls]

    def get_filly_rolls_active_filter(self,
                                      # TODO the inputs should be cleaned by the api layer (ie strs should be all lowercase and stripped)
                                      type=None,
                                      type_id=None,
                                      brand=None,
                                      brand_id=None,
                                      surface=None,
                                      surface_id=None,
                                      color=None,
                                      color_id=None,
                                      subtype=None,
                                      subtype_id=None,
                                      opened=None,
                                      in_use=None,
                                      ):
        """Get all in use filament rolls (on the printer) with optional filters.

        Args:
            type (str, optional): Filament type name to filter by.
            type_id (int, optional): Filament type ID to filter by.
            brand (str, optional): Filament brand name to filter by.
            brand_id (int, optional): Filament brand ID to filter by.
            surface (str, optional): Filament surface name to filter by.
            surface_id (int, optional): Filament surface ID to filter by.
            color (str, optional): Filament color name to filter by.
            color_id (int, optional): Filament color ID to filter by.
            subtype (str, optional): Filament subtype name to filter by.
            subtype_id (int, optional): Filament subtype ID to filter by.
            opened (bool, optional): Filter by opened status.
            in_use (bool, optional): Filter by in use status.
        """
        with self.get_session() as session:
            query = session.query(db_filly_roll).filter(db_filly_roll.weight_grams > 0)

            if type:
                query = query.join(db_filly_types).filter(db_filly_types.name == type)
            if type_id:
                query = query.filter(db_filly_roll.type_id == type_id)
            if brand:
                query = query.join(db_filly_brands).filter(db_filly_brands.name == brand)
            if brand_id:
                query = query.filter(db_filly_roll.brand_id == brand_id)
            if surface:
                query = query.join(db_filly_surfaces).filter(db_filly_surfaces.name == surface)
            if surface_id:
                query = query.filter(db_filly_roll.surface_id == surface_id)
            if color:
                query = query.join(db_filly_colors).filter(db_filly_colors.name == color)
            if color_id:
                query = query.filter(db_filly_roll.color_id == color_id)
            if subtype:
                query = query.join(db_filly_subtypes).filter(db_filly_subtypes.name == subtype)
            if subtype_id:
                query = query.filter(db_filly_roll.subtype_id == subtype_id)
            if opened is not None:
                query = query.filter(db_filly_roll.opened == opened)
            if in_use is not None:
                query = query.filter(db_filly_roll.in_use == in_use)

            rolls = query.all()
            return [roll.to_dict() for roll in rolls]

    def get_filly_types(self):
        """Get all filament types.

        Returns:
            Dict of filament types
        """
        with self.get_session() as session:
            types = session.query(db_filly_types).all()
            return [t.to_dict() for t in types]

    def get_filly_brands(self):
        """Get all filament brands.

        Returns:
            Dict of filament brands
        """
        with self.get_session() as session:
            brands = session.query(db_filly_brands).all()
            return [b.to_dict() for b in brands]

    def get_filly_surfaces(self):
        """Get all filament surfaces.

        Returns:
            Dict of filament surfaces
        """
        with self.get_session() as session:
            surfaces = session.query(db_filly_surfaces).all()
            return [s.to_dict() for s in surfaces]

    def get_filly_colors(self):
        """Get all filament colors.

        Returns:
            Dict of filament colors
        """
        with self.get_session() as session:
            colors = session.query(db_filly_colors).all()
            return [c.to_dict() for c in colors]

    def get_filly_subtypes(self):
        """Get all filament subtypes.

        Returns:
            Dict of filament subtypes
        """
        with self.get_session() as session:
            subtypes = session.query(db_filly_subtypes).all()
            return [s.to_dict() for s in subtypes]

    def insert_dummy_filly_roll(self):
        """Insert a dummy filly roll for testing purposes."""
        with self.get_session() as session:
            dummy_roll = db_filly_roll(
                type_id=1,
                brand_id=1,
                surface_id=1,
                color_id=1,
                subtype_id=1,
                weight_grams=500,
                original_weight_grams=1000,
                opened=True,
                in_use=False
            )
            session.add(dummy_roll)
            print("Inserted dummy filly roll for testing.")

def main():
    """Main function to test database connection and configuration."""
    print("=" * 60)
    print("Database Configuration Test")
    print("=" * 60)
    print(f"DB_TYPE: {DB_TYPE}")
    print("=" * 60)

    try:
        # Initialize database connection
        db = db_connect()
        print("\n✓ Database connection initialized successfully!")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
