
import os
import sys
# change dir to common folder
os.chdir(os.path.dirname(os.path.dirname(__file__))) # change to 2 levels up (common folder)
# Add the common directory to Python's import path
common_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, common_path)

from db_classes import (
    db_filly_types,
    db_filly_brands,
    db_filly_colors,
    db_filly_subtypes,
    db_filly_roll
)

def test_db_filly_brands_to_dict():
    """Test the to_dict method of db_filly_brands class."""
    brand = db_filly_brands()
    brand.id = 1
    brand.name = "testbrand"

    brand_dict = brand.to_dict()

    assert brand_dict['id'] == 1
    assert brand_dict['name'] == "testbrand"

def test_db_filly_brands_name():
    """Test the name_formatted property of db_filly_brands class."""
    brand = db_filly_brands()
    brand.id = 1
    brand.name = "test brand"

    assert brand.name_formatted == "Test Brand"
    assert brand.descriptive_name == "Test Brand (ID: 1)"

def test_db_filly_types_to_dict():
    """Test the to_dict method of db_filly_types class."""
    filly_type = db_filly_types()
    filly_type.id = 2
    filly_type.name = "testtype"

    type_dict = filly_type.to_dict()

    assert type_dict['id'] == 2
    assert type_dict['name'] == "testtype"

def test_db_filly_types_name():
    """Test the name_formatted property of db_filly_types class."""
    filly_type = db_filly_types()
    filly_type.id = 2
    filly_type.name = "test type"

    assert filly_type.name_formatted == "TEST TYPE"
    assert filly_type.descriptive_name == "TEST TYPE (ID: 2)"

def test_db_filly_subtypes_to_dict():
    """Test the to_dict method of db_filly_subtypes class."""
    subtype = db_filly_subtypes()
    subtype.id = 3
    subtype.name = "testsubtype"

    subtype_dict = subtype.to_dict()

    assert subtype_dict['id'] == 3
    assert subtype_dict['name'] == "testsubtype"

def test_db_filly_subtypes_name():
    """Test the name_formatted property of db_filly_subtypes class."""
    subtype = db_filly_subtypes()
    subtype.id = 3
    subtype.name = "test subtype"

    assert subtype.name_formatted == "Test Subtype"
    assert subtype.descriptive_name == "Test Subtype (ID: 3)"

def test_db_filly_colors_to_dict():
    """Test the to_dict method of db_filly_colors class."""
    color = db_filly_colors()
    color.id = 4
    color.name = "testcolor"

    color_dict = color.to_dict()

    assert color_dict['id'] == 4
    assert color_dict['name'] == "testcolor"

def test_db_filly_colors_name():
    """Test the name_formatted property of db_filly_colors class."""
    color = db_filly_colors()
    color.id = 4
    color.name = "test color"

    assert color.name_formatted == "Test Color"
    assert color.descriptive_name == "Test Color (ID: 4)"

def test_db_filly_roll_to_dict():
    """Test the to_dict method of db_filly_roll class."""
    roll = db_filly_roll()
    roll.id = 6
    roll.type_id = 1
    roll.brand_id = 2
    roll.color_id = 4
    roll.subtype_id = 5

    roll_dict = roll.to_dict()

    assert roll_dict['id'] == 6
    assert roll_dict['type_id'] == 1
    assert roll_dict['brand_id'] == 2
    assert roll_dict['color_id'] == 4
    assert roll_dict['subtype_id'] == 5

def test_db_filly_roll_name():
    """Test the name_formatted property of db_filly_roll class."""
    roll = db_filly_roll()
    roll.id = 6
    roll.type_id = 1
    roll.brand_id = 2
    roll.color_id = 4
    roll.subtype_id = 5
    roll.original_weight_grams = 1000.0
    roll.weight_grams = 100.0
    roll.opened = True
    roll.in_use = False

    type_obj = db_filly_types()
    type_obj.name = "pla"
    type_obj.id = 1
    roll.type = type_obj
    brand_obj = db_filly_brands()
    brand_obj.name = "bambu"
    brand_obj.id = 2
    roll.brand = brand_obj
    color_obj = db_filly_colors()
    color_obj.name = "red"
    color_obj.id = 4
    roll.color = color_obj
    subtype_obj = db_filly_subtypes()
    subtype_obj.name = "basic"
    subtype_obj.id = 5
    roll.subtype = subtype_obj

    assert roll.descriptive_name == "[ID: 6] Bambu PLA-Basic, Red (100.0/1000.0g). Opened: True. In Use: False"
