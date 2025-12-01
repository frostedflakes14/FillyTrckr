# Common Module

This directory contains shared Python code used by both the frontend and backend services of FillyTrckr.

## Contents

### Core Files

- **config.py** - Application configuration loader
  - Loads settings from JSON config files or environment variables
  - Manages database, API, and application settings
  - See `config_example.json` and `config_example.env` for templates

- **common_logging.py** - Centralized logging configuration
  - Provides configured logger instances for consistent logging across services
  - Writes to both console and log files (`logs/fillytrckr.log`)
  - Usage: `from common_logging import get_logger`

### Database

- **db_base.py** - SQLAlchemy declarative base
  - Foundation for all database models

- **db_classes.py** - SQLAlchemy ORM models
  - Database table definitions for:
    - `db_filly_types` - Filament types (PLA, ABS, PETG, TPU, etc.)
    - `db_filly_brands` - Filament brands
    - `db_filly_colors` - Filament colors
    - `db_filly_subtypes` - Filament subtypes (silk, matte, etc.)
    - `db_filly_rolls` - Individual filament roll records

- **populate_default_tables.py** - Default data for database initialization
  - Contains default lists for types, brands, colors, and subtypes
  - Used during initial database setup

### Configuration Templates

- **config_example.json** - JSON configuration template
- **config_example.env** - Environment variable configuration template

## Usage

Import shared modules in backend or other services:

```python
# Configuration
from config import filly_trkr_config
config = filly_trkr_config()

# Logging
from common_logging import get_logger
logger = get_logger(__name__)

# Database models
from db_classes import db_filly_rolls, db_filly_types, db_filly_brands
from db_base import Base
```

## Testing

The `test/` directory contains unit tests for the common module components.
