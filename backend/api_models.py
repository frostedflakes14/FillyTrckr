
from pydantic import BaseModel, model_validator
from typing import Optional


class request_roll_set_in_use(BaseModel):
    in_use: bool = True
    class Config:
        json_schema_extra = {
            "example": {
                "in_use": True
            }
        }

class request_roll_duplicate(BaseModel):
    original_weight_grams: Optional[float] = None

    class Config:
        json_schema_extra = {
            "example": {
                "original_weight_grams": 1000.0
            }
        }

class request_roll_update_weight(BaseModel):
    new_weight_grams: Optional[float] = None
    decrease_by_grams: Optional[float] = None

    @model_validator(mode='after')
    def check_at_least_one_field(self):
        if self.new_weight_grams is None and self.decrease_by_grams is None:
            raise ValueError('Either new_weight_grams or decrease_by_grams must be provided')
        if self.new_weight_grams is not None and self.decrease_by_grams is not None:
            raise ValueError('Only one of new_weight_grams or decrease_by_grams can be provided, not both')
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "new_weight_grams": 500.0
            }
        }

class response_get_brands(BaseModel):
    brands: list[dict]
    class Config:
        json_schema_extra = {
            "example": {
                "brands": [
                    {
                        "id": 1,
                        "name": "bambu",
                        "created_at": "2024-01-01T12:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "prusa",
                        "created_at": "2024-01-02T12:00:00Z"
                    }
                ]
            }
        }

class response_get_types(BaseModel):
    types: list[dict]
    class Config:
        json_schema_extra = {
            "example": {
                "types": [
                    {
                        "id": 1,
                        "name": "pla",
                        "created_at": "2024-01-01T12:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "abs",
                        "created_at": "2024-01-02T12:00:00Z"
                    }
                ]
            }
        }
class response_get_colors(BaseModel):
    colors: list[dict]
    class Config:
        json_schema_extra = {
            "example": {
                "colors": [
                    {
                        "id": 1,
                        "name": "red",
                        "created_at": "2024-01-01T12:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "blue",
                        "created_at": "2024-01-02T12:00:00Z"
                    }
                ]
            }
        }
class response_get_subtypes(BaseModel):
    subtypes: list[dict]
    class Config:
        json_schema_extra = {
            "example": {
                "subtypes": [
                    {
                        "id": 1,
                        "name": "silk",
                        "created_at": "2024-01-01T12:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "high flow",
                        "created_at": "2024-01-02T12:00:00Z"
                    }
                ]
            }
        }

class response_get_surfaces(BaseModel):
    surfaces: list[dict]
    class Config:
        json_schema_extra = {
            "example": {
                "surfaces": [
                    {
                        "id": 1,
                        "name": "basic",
                        "created_at": "2024-01-01T12:00:00Z"
                    },
                    {
                        "id": 2,
                        "name": "matte",
                        "created_at": "2024-01-02T12:00:00Z"
                    }
                ]
            }
        }

class response_roll_data(BaseModel):
    id: int
    type: str
    type_id: int
    brand: str
    brand_id: int
    surface: str
    surface_id: int
    color: str
    color_id: int
    subtype: str
    subtype_id: int
    weight_grams: float
    original_weight_grams: float
    opened: bool
    in_use: bool
    created_at: str
    updated_at: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "type": "PLA",
                "type_id": 1,
                "brand": "bambu",
                "brand_id": 1,
                "surface": "matte",
                "surface_id": 1,
                "color": "blue",
                "color_id": 1,
                "subtype": "basic",
                "subtype_id": 1,
                "weight_grams": 750,
                "original_weight_grams": 1000,
                "opened": True,
                "in_use": True,
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-02T12:00:00Z"
            }
        }

class response_get_rolls(BaseModel):
    rolls: list[response_roll_data]
    class Config:
        json_schema_extra = {
            "example": {
                "rolls": [
                    {
                        "id": 1,
                        "type": "pla",
                        "type_id": 1,
                        "brand": "bambu",
                        "brand_id": 1,
                        "surface": "matte",
                        "surface_id": 1,
                        "color": "blue",
                        "color_id": 1,
                        "subtype": "basic",
                        "subtype_id": 1,
                        "weight_grams": 750,
                        "original_weight_grams": 1000,
                        "opened": True,
                        "in_use": True,
                        "created_at": "2024-01-01T12:00:00Z",
                        "updated_at": "2024-01-02T12:00:00Z"
                    }
                ]
            }
        }

class response_roll_update(BaseModel):
    result: bool
    roll_data: response_roll_data

    class Config:
        json_schema_extra = {
            "example": {
                "result": True,
                "roll_data": {
                    "id": 1,
                    "type": "PLA",
                    "type_id": 1,
                    "brand": "bambu",
                    "brand_id": 1,
                    "surface": "matte",
                    "surface_id": 1,
                    "color": "blue",
                    "color_id": 1,
                    "subtype": "basic",
                    "subtype_id": 1,
                    "weight_grams": 750,
                    "original_weight_grams": 1000,
                    "opened": True,
                    "in_use": True,
                    "created_at": "2024-01-01T12:00:00Z",
                    "updated_at": "2024-01-02T12:00:00Z"
                }
            }
        }