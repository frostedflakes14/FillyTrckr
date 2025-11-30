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
from config import filly_trkr_config
from common_logging import get_logger
from db_base import Base
from db_classes import (
    db_filly_types,
    db_filly_brands,
    db_filly_colors,
    db_filly_subtypes,
    db_filly_roll
)
from populate_default_tables import (
    filly_types_defaults,
    filly_brands_defaults,
    filly_colors_defaults,
    filly_subtypes_defaults
)

logger = get_logger()

def default_roll_result():
    # TODO define an error statement item?
    return {'result': False, 'roll_data': {}}

class db_connect:
    """Database connection manager class.

    Handles database initialization, connection management, and provides
    methods for querying and inserting data.
    """

    def __init__(self, config=filly_trkr_config()):
        """Initialize the database connection.

        Creates the engine, initializes schema if needed, and populates
        default data. Does not maintain an open session.
        """
        self.engine = None
        self.SessionLocal = None
        self._config = config
        self.db_connected = False
        self._initialize_database()

    def _initialize_database(self):
        """Internal method to set up the database engine and schema."""
        logger.info("Initializing database...")
        db_url = self._config.database_info._db_connection_string
        if self._config.database_info.type == 'sqlite':
            # Ensure the database directory exists
            db_dir = self._config.database_info.db_dir
            os.makedirs(db_dir, exist_ok=True)

        try:
            self.engine = create_engine(db_url, echo=False)
            # Test the connection
            with self.engine.connect() as conn:
                logger.info("Successfully connected to database.")
                self.db_connected = True
        except OperationalError as e:
            logger.error(f"Failed to connect to database. Error: {str(e)}")
            raise ConnectionError(
                f"Failed to connect to database. Error: {str(e)}"
            ) from e

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
        logger.info("Populating default data...")

        with self.get_session() as session:
            added_count = 0

            # Make sure the tables exist before querying, if they don't exist, create them
            Base.metadata.create_all(self.engine)

            # Get all existing names in one query per table
            existing_types = {row.name for row in session.query(db_filly_types.name).all()}
            existing_brands = {row.name for row in session.query(db_filly_brands.name).all()}
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
                logger.info(f"Added {added_count} new default entries.")
            else:
                logger.info("All default data already exists. No new entries added.")

    # Database query methods

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
            color (str, optional): Filament color name to filter by.
            color_id (int, optional): Filament color ID to filter by.
            subtype (str, optional): Filament subtype name to filter by.
            subtype_id (int, optional): Filament subtype ID to filter by.
            opened (bool, optional): Filter by opened status.
            in_use (bool, optional): Filter by in use status.
        """
        logger.info(f'Getting active filly rolls with filters: type={type}, type_id={type_id}, brand={brand}, brand_id={brand_id}, color={color}, color_id={color_id}, subtype={subtype}, subtype_id={subtype_id}, opened={opened}, in_use={in_use}')
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

    # Database insert methods

    # TODO remove - this is a dummy function
    def insert_dummy_filly_roll(self):
        """Insert a dummy filly roll for testing purposes."""
        with self.get_session() as session:
            dummy_roll = db_filly_roll(
                type_id=1,
                brand_id=1,
                color_id=1,
                subtype_id=1,
                weight_grams=500,
                original_weight_grams=1000,
                opened=True,
                in_use=False
            )
            session.add(dummy_roll)
            logger.info("Inserted dummy filly roll for testing.")

    def insert_roll(self,
                    type_id,
                    brand_id,
                    color_id,
                    subtype_id,
                    original_weight_grams,
                    weight_grams=None,
                    opened=False,
                    in_use=False):
        """Insert a new filly roll into the database.

        Args:
            type_id (int): Filament type ID.
            brand_id (int): Filament brand ID.
            color_id (int): Filament color ID.
            subtype_id (int): Filament subtype ID.
            original_weight_grams (float): Original weight in grams.
            weight_grams (float, optional): Current weight in grams, if left as None, set to original_weight_grams. Defaults to None.
            opened (bool, optional): Whether the roll is opened. Defaults to False.
            in_use (bool, optional): Whether the roll is in use. Defaults to False.
        """
        logger.info(f'Inserting new filly roll: type_id={type_id}, brand_id={brand_id}, color_id={color_id}, subtype_id={subtype_id}, original_weight_grams={original_weight_grams}, weight_grams={weight_grams}, opened={opened}, in_use={in_use}')
        roll_data = default_roll_result()
        with self.get_session() as session:
            if weight_grams is None:
                weight_grams = original_weight_grams
            new_roll = db_filly_roll(
                type_id=type_id,
                brand_id=brand_id,
                color_id=color_id,
                subtype_id=subtype_id,
                weight_grams=weight_grams,
                original_weight_grams=original_weight_grams,
                opened=opened,
                in_use=in_use
            )
            session.add(new_roll)
            session.flush()  # This assigns the ID and makes relationships accessible
            logger.info(f"Successfully inserted new filly roll: {new_roll.descriptive_name}")

            # Get the roll data before session closes
            roll_data['roll_data'] = new_roll.to_dict()
            roll_data['result'] = True

        return roll_data

    def insert_dup_roll(self, roll_id, original_weight_grams=1000):
        """Insert a duplicate of an existing filly roll.

        Args:
            roll_id (int): ID of the filly roll to duplicate.
            original_weight_grams (float, optional): Original weight for the new roll. Defaults to 1000.
        """
        roll_data = default_roll_result()
        with self.get_session() as session:
            original_roll = session.query(db_filly_roll).filter_by(id=roll_id).first()
            if not original_roll:
                logger.error(f"No filly roll found with ID {roll_id}. Cannot duplicate.")
                return roll_data

            dup_roll = db_filly_roll(
                type_id=original_roll.type_id,
                brand_id=original_roll.brand_id,
                color_id=original_roll.color_id,
                subtype_id=original_roll.subtype_id,
                weight_grams=original_weight_grams,
                original_weight_grams=original_weight_grams,
                opened=False,
                in_use=False
            )
            session.add(dup_roll)
            session.flush()  # This assigns the ID and makes relationships accessible
            logger.info(f"Successfully duplicated filly roll: {dup_roll.descriptive_name}")
            roll_data['roll_data'] = dup_roll.to_dict()
            roll_data['result'] = True
        return roll_data

    def open_roll(self, roll_id):
        """Mark a filly roll as opened.

        Args:
            roll_id (int): ID of the filly roll to mark as opened.
        """
        roll_data = default_roll_result()
        with self.get_session() as session:
            roll = session.query(db_filly_roll).filter_by(id=roll_id).first()
            if not roll:
                logger.error(f"No filly roll found with ID {roll_id}. Cannot open.")
                return roll_data

            roll.opened = True
            logger.info(f"Marked filly roll as opened: {roll.descriptive_name}")
            roll_data['roll_data'] = roll.to_dict()
            roll_data['result'] = True

        return roll_data

    def change_in_use_status(self, roll_id, in_use):
        """Change the in_use status of a filly roll.

        Args:
            roll_id (int): ID of the filly roll to update.
            in_use (bool): New in_use status.
        """
        roll_data = default_roll_result()
        with self.get_session() as session:
            roll = session.query(db_filly_roll).filter_by(id=roll_id).first()
            if not roll:
                logger.error(f"No filly roll found with ID {roll_id}. Cannot change in_use status.")
                return roll_data

            roll.in_use = in_use
            status_str = "in use" if in_use else "not in use"
            logger.info(f"Set filly roll as {status_str}: {roll.descriptive_name}")
            roll_data['roll_data'] = roll.to_dict()
            roll_data['result'] = True
        return roll_data

    def update_roll_weight(self, roll_id, new_weight_grams=None, decr_weight_grams=None):
        """Update the weight of a filly roll.

        Args:
            roll_id (int): ID of the filly roll to update.
            new_weight_grams (float, optional): New weight in grams. Defaults to None.
            decr_weight_grams (float, optional): Amount to decrease weight by. Defaults to None.
        """
        roll_data = default_roll_result()
        with self.get_session() as session:
            roll = session.query(db_filly_roll).filter_by(id=roll_id).first()
            if not roll:
                logger.error(f"No filly roll found with ID {roll_id}. Cannot update weight.")
                return roll_data

            if new_weight_grams is not None:
                roll.weight_grams = new_weight_grams
                roll_data['roll_data'] = roll.to_dict()
                roll_data['result'] = True
            elif decr_weight_grams is not None:
                roll.weight_grams = max(0, roll.weight_grams - decr_weight_grams)
                roll_data['roll_data'] = roll.to_dict()
                roll_data['result'] = True
            else:
                logger.error("No weight update parameters provided.")
                return roll_data

            logger.info(f"Updated weight of filly roll to {roll.weight_grams}: {roll.descriptive_name}")
        return roll_data

def main():
    """Main function to test database connection and configuration."""
    print("=" * 60)
    print("Database Configuration Test")
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
