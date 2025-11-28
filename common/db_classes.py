
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Double, ForeignKey, JSON, DateTime, BigInteger
from sqlalchemy import select, over
from sqlalchemy.sql import func
from db_base import Base

from sqlalchemy.orm import relationship, aliased


# class DEFAULT(Base):
#     __tablename__ = 'filly_type'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     is_active = Column(Boolean, nullable=False, default=True)
#     created_at = Column(DateTime, nullable=False, server_default=func.now(), timezone=True)


class db_filly_types(Base):
    """Filament types: PLA, ABS, PETG, TPU, etc."""
    __tablename__ = 'filly_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), timezone=True)

class db_filly_brands(Base):
    """Filament brands: Bambu, Sunlu, Inland, Prusament, eSun, etc."""
    __tablename__ = 'filly_brands'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), timezone=True)

class db_filly_surfaces(Base):
    """Filament surface types: Basic/Normal, Matte, Silk, Metal, Wood.
    Silk is different from the subtype Silk"""
    __tablename__ = 'filly_surfaces'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), timezone=True)

class db_filly_colors(Base):
    """Filament color options. Most should be Red, Blue, Green, etc. But some could be multi-color or special colors, like wood type"""
    __tablename__ = 'filly_colors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # TODO maybe add hex code column later
    created_at = Column(DateTime, nullable=False, server_default=func.now(), timezone=True)


class db_filly_subtypes(Base):
    """Filament subtypes: HF, Silk, Plus, Metal, wood, etc."""
    __tablename__ = 'filly_subtypes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), timezone=True)


class db_filly_roll(Base):
    """Filly roll table"""
    __tablename__ = 'filly_rolls'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('filly_types.id'), nullable=False)
    brand_id = Column(Integer, ForeignKey('filly_brands.id'), nullable=False)
    surface_id = Column(Integer, ForeignKey('filly_surfaces.id'), nullable=False)
    color_id = Column(Integer, ForeignKey('filly_colors.id'), nullable=False)
    subtype_id = Column(Integer, ForeignKey('filly_subtypes.id'), nullable=True)
    weight_grams = Column(Double) # current weight, will be updated. After its 0 or below, the roll is considered empty
    original_weight_grams = Column(Double) # shouldn't be changed after creation
    opened = Column(Boolean, nullable=False, default=False)
    is_active = Column(Boolean, nullable=False, default=False) # on the printer
    created_at = Column(DateTime, nullable=False, server_default=func.now(), timezone=True)
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), timezone=True)

    type = relationship("filly_types")
    brand = relationship("filly_brands")
    surface = relationship("filly_surfaces")
    color = relationship("filly_colors")
    subtype = relationship("filly_subtypes")