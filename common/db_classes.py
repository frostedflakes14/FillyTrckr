
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
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @property
    def name_formatted(self):
        return self.name.upper()

    @property
    def descriptive_name(self):
        return f"{self.name_formatted} (ID: {self.id})"

    def __repr__(self):
        return f"<Class {self.__class__.__name__}> {self.descriptive_name}"

    def to_dict(self):
        """Convert the filly type to a dictionary representation.

        Returns:
            Dictionary containing type information
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class db_filly_brands(Base):
    """Filament brands: Bambu, Sunlu, Inland, Prusament, eSun, etc."""
    __tablename__ = 'filly_brands'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @property
    def name_formatted(self):
        return self.name.title()

    @property
    def descriptive_name(self):
        return f"{self.name_formatted} (ID: {self.id})"

    def __repr__(self):
        return f"<Class {self.__class__.__name__}> {self.descriptive_name}"

    def to_dict(self):
        """Convert the filly type to a dictionary representation.

        Returns:
            Dictionary containing type information
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class db_filly_colors(Base):
    """Filament color options. Most should be Red, Blue, Green, etc. But some could be multi-color or special colors, like wood type"""
    __tablename__ = 'filly_colors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # TODO maybe add hex code column later
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @property
    def name_formatted(self):
        return self.name.title()

    @property
    def descriptive_name(self):
        return f"{self.name_formatted} (ID: {self.id})"

    def __repr__(self):
        return f"<Class {self.__class__.__name__}> {self.descriptive_name}"

    def to_dict(self):
        """Convert the filly type to a dictionary representation.

        Returns:
            Dictionary containing type information
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class db_filly_subtypes(Base):
    """Filament subtypes: HF, Silk, Plus, Metal, wood, etc."""
    __tablename__ = 'filly_subtypes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    @property
    def name_formatted(self):
        return self.name.title()

    @property
    def descriptive_name(self):
        return f"{self.name_formatted} (ID: {self.id})"

    def __repr__(self):
        return f"<Class {self.__class__.__name__}> {self.descriptive_name}"

    def to_dict(self):
        """Convert the filly type to a dictionary representation.

        Returns:
            Dictionary containing type information
        """
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }

class db_filly_roll(Base):
    """Filly roll table"""
    __tablename__ = 'filly_rolls'

    id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('filly_types.id'), nullable=False)
    brand_id = Column(Integer, ForeignKey('filly_brands.id'), nullable=False)
    color_id = Column(Integer, ForeignKey('filly_colors.id'), nullable=False)
    subtype_id = Column(Integer, ForeignKey('filly_subtypes.id'), nullable=True)
    weight_grams = Column(Double) # current weight, will be updated. After its 0 or below, the roll is considered empty
    original_weight_grams = Column(Double) # shouldn't be changed after creation
    opened = Column(Boolean, nullable=False, default=False)
    in_use = Column(Boolean, nullable=False, default=False) # on the printer
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    type = relationship("db_filly_types")
    brand = relationship("db_filly_brands")
    color = relationship("db_filly_colors")
    subtype = relationship("db_filly_subtypes")

    @property
    def descriptive_name(self):
        return f"[ID: {self.id}] {self.brand.name_formatted} {self.type.name_formatted}-{self.subtype.name_formatted}, {self.color.name_formatted} ({self.weight_grams}/{self.original_weight_grams}g). Opened: {self.opened}. In Use: {self.in_use}"

    def __repr__(self):
        return f"<Class {self.__class__.__name__}> {self.descriptive_name}"
    def to_dict(self):
        """Convert the filly roll to a dictionary representation.

        Returns:
            Dictionary containing roll information with related data
        """
        return {
            'id': self.id,
            'type': self.type.name if self.type else None,
            'type_id': self.type_id,
            'brand': self.brand.name if self.brand else None,
            'brand_id': self.brand_id,
            'color': self.color.name if self.color else None,
            'color_id': self.color_id,
            'subtype': self.subtype.name if self.subtype else None,
            'subtype_id': self.subtype_id,
            'weight_grams': self.weight_grams,
            'original_weight_grams': self.original_weight_grams,
            'opened': self.opened,
            'in_use': self.in_use,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
