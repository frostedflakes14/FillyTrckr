"""Database configuration and initialization module.

Supports both SQLite (for development) and PostgreSQL (for production).
Database type and credentials are configurable via environment variables.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fillytrckr")

# SQLite database path
SQLITE_DB_PATH = Path(__file__).parent.parent / "example.db"


def create_database_engine():
    """Create and return a SQLAlchemy engine based on DB_TYPE configuration."""

    if DB_TYPE == "sqlite":
        # SQLite configuration
        db_url = f"sqlite:///{SQLITE_DB_PATH}"
        print(f"Using SQLite database at: {SQLITE_DB_PATH}")
        engine = create_engine(db_url, echo=False)

        # Check if database exists, if not create it
        if not SQLITE_DB_PATH.exists():
            print("Database does not exist. Creating new SQLite database...")
            Base.metadata.create_all(engine)
            print("Database schema created successfully.")
        else:
            print("Existing SQLite database found.")

        # Always populate default data (only adds missing entries)
        populate_default_data(engine)

        return engine

    elif DB_TYPE in ["postgres", "postgresql"]:
        # PostgreSQL configuration
        if not DB_USERNAME or not DB_PASSWORD:
            raise ValueError(
                "PostgreSQL requires DB_USERNAME and DB_PASSWORD environment variables to be set."
            )

        db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        print(f"Attempting to connect to PostgreSQL database at {DB_HOST}:{DB_PORT}/{DB_NAME}")

        try:
            engine = create_engine(db_url, echo=False)
            # Test the connection
            with engine.connect() as conn:
                print("Successfully connected to PostgreSQL database.")

            # Always populate default data (only adds missing entries)
            populate_default_data(engine)

            return engine
        except OperationalError as e:
            raise ConnectionError(
                f"Failed to connect to PostgreSQL database. Error: {str(e)}"
            ) from e

    else:
        raise ValueError(
            f"Unsupported DB_TYPE: {DB_TYPE}. Supported types are 'sqlite', 'postgres', or 'postgresql'."
        )


def populate_default_data(engine):
    """Populate default data into the database tables.

    Only adds entries that don't already exist (checks by name).
    Safe to run multiple times without creating duplicates.
    Uses efficient bulk queries to check existing entries.
    """
    print("Populating default data...")
    Session = sessionmaker(bind=engine)
    session = Session()

    added_count = 0

    try:
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

        session.commit()
        if added_count > 0:
            print(f"Added {added_count} new default entries.")
        else:
            print("All default data already exists. No new entries added.")
    except Exception as e:
        session.rollback()
        print(f"Error populating default data: {str(e)}")
        raise
    finally:
        session.close()


def get_session():
    """Create and return a new database session."""
    engine = create_database_engine()
    Session = sessionmaker(bind=engine)
    return Session()


if __name__ == "__main__":
    # Test the database connection
    print("=" * 60)
    print("Database Configuration Test")
    print("=" * 60)
    print(f"DB_TYPE: {DB_TYPE}")
    print(f"DB_USERNAME: {'***' if DB_USERNAME else 'None'}")
    print(f"DB_PASSWORD: {'***' if DB_PASSWORD else 'None'}")
    print("=" * 60)

    try:
        engine = create_database_engine()
        print("\n✓ Database engine created successfully!")

        # Test session creation
        session = get_session()
        print("✓ Database session created successfully!")

        # Query to check if tables have data
        if DB_TYPE == "sqlite":
            types_count = session.query(db_filly_types).count()
            print(f"✓ Found {types_count} filament types in database")

        session.close()
        print("\n" + "=" * 60)
        print("Database configuration test completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)
