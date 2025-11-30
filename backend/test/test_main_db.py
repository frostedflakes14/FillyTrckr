
import os
import sys
import pytest
# change dir to backend folder
# Add the backend directory to Python's import path
test_path = os.path.dirname(os.path.abspath(__file__))
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
common_path = os.path.join(os.path.dirname(backend_path), "common")
os.chdir(backend_path) # change to 2 levels up (backend folder)
sys.path.insert(0, common_path)
sys.path.insert(0, backend_path)

from main_db import db_connect
from config import filly_trkr_config

@pytest.fixture(scope="session", autouse=True)
def delete_test_db_files():
    """Fixture to delete test database files before"""
    # Before tests
    test_db_files = [
        os.path.join(test_path, "test_sqlite_db_connection.db"),
    ]
    for db_file in test_db_files:
        if os.path.exists(db_file):
            os.remove(db_file)

@pytest.fixture()
def test_config():
    """Fixture to provide a test configuration."""
    config = filly_trkr_config(os.path.join(test_path, "test_config_db_connection.json"))
    return config

@pytest.fixture()
def db_connection(test_config):
    """Fixture to provide a database connection."""
    # This should populate the sqlite database with default data, which we can use for testing
    db = db_connect(test_config)
    if not db.db_connected:
        pytest.fail("Failed to connect to the database")
    return db

def test_db_connection(db_connection):
    """Test that the database connection is established."""
    assert db_connection.db_connected, "Database connection should be established"

def test_get_brands(db_connection):
    """Test the get_filly_brands method."""
    brands = db_connection.get_filly_brands()
    assert isinstance(brands, list), "Brands should be a list"
    # brands should be a list of dicts, each with 'id' and 'name' keys
    # should have these brands: bambu, sunlu, inland
    expected_brands = ["bambu", "sunlu", "inland"]
    # reformat brands to a list of names
    brand_names = [brand['name'] for brand in brands]
    assert all(name in brand_names for name in expected_brands), "Brands should include bambu, sunlu, and inland"

def test_get_types(db_connection):
    """Test the get_filly_types method."""
    types = db_connection.get_filly_types()
    assert isinstance(types, list), "Types should be a list"
    # types should be a list of dicts, each with 'id' and 'name' keys
    # should have these types: PLA, ABS, PETG
    expected_types = ["pla", "abs", "petg"]
    # reformat types to a list of names
    type_names = [type['name'] for type in types]
    assert all(name in type_names for name in expected_types), "Types should include PLA, ABS, and PETG"

def test_get_colors(db_connection):
    """Test the get_filly_colors method."""
    colors = db_connection.get_filly_colors()
    assert isinstance(colors, list), "Colors should be a list"
    # colors should be a list of dicts, each with 'id' and 'name' keys
    # should have these colors: red, blue, green
    expected_colors = ["red", "blue", "green"]
    # reformat colors to a list of names
    color_names = [color['name'] for color in colors]
    assert all(name in color_names for name in expected_colors), "Colors should include red, blue, and green"

def test_get_subtypes(db_connection):
    """Test the get_filly_subtypes method."""
    subtypes = db_connection.get_filly_subtypes()
    assert isinstance(subtypes, list), "Subtypes should be a list"
    # subtypes should be a list of dicts, each with 'id' and 'name' keys
    # should have these subtypes: silk, high flow, matte
    expected_subtypes = ["silk", "high flow", "matte"]
    # reformat subtypes to a list of names
    subtype_names = [subtype['name'] for subtype in subtypes]
    assert all(name in subtype_names for name in expected_subtypes), "Subtypes should include silk, high flow, and matte"

def test_insert_rolls(db_connection):
    """Test the get_filly_rolls_all method."""
    rolls = db_connection.get_filly_rolls_all()
    assert len(rolls) == 0 # no rolls to start

    # Insert a test roll
    insert_result = db_connection.insert_roll(
        type_id=1,
        brand_id=1,
        color_id=1,
        subtype_id=1,
        original_weight_grams=1000.0,
        weight_grams=500.0,
        opened=True,
        in_use=False
    )
    assert insert_result.get('result', False), "Roll insertion should be successful"

    # check that the roll matches what was inserted
    rolls = db_connection.get_filly_rolls_all()
    assert len(rolls) == 1, "There should be one roll after insertion"
    roll = rolls[0]
    assert roll['type_id'] == 1
    assert roll['brand_id'] == 1
    assert roll['color_id'] == 1
    assert roll['subtype_id'] == 1
    assert roll['original_weight_grams'] == 1000.0
    assert roll['weight_grams'] == 500.0
    assert roll['opened'] is True
    assert roll['in_use'] is False

    # check that the insert result is the same
    assert roll['type_id'] == insert_result['roll_data']['type_id']
    assert roll['brand_id'] == insert_result['roll_data']['brand_id']
    assert roll['color_id'] == insert_result['roll_data']['color_id']
    assert roll['subtype_id'] == insert_result['roll_data']['subtype_id']
    assert roll['original_weight_grams'] == insert_result['roll_data']['original_weight_grams']
    assert roll['weight_grams'] == insert_result['roll_data']['weight_grams']
    assert roll['opened'] is insert_result['roll_data']['opened']
    assert roll['in_use'] is insert_result['roll_data']['in_use']

def test_insert_dup_roll(db_connection):
    """Test the insert_dup_roll method."""
    # Insert a test roll to duplicate
    insert_result = db_connection.insert_roll(
        type_id=2,
        brand_id=2,
        color_id=2,
        subtype_id=2,
        original_weight_grams=1000.0,
        weight_grams=500.0,
        opened=False,
        in_use=False
    )
    assert insert_result.get('result', False), "Roll insertion should be successful"
    original_roll_id = insert_result['roll_data']['id']

    # Duplicate the roll
    dup_result = db_connection.insert_dup_roll(original_roll_id, original_weight_grams=2000.0)
    assert dup_result.get('result', False), "Roll duplication should be successful"

    original_roll = db_connection.get_filly_roll_id(insert_result['roll_data']['id'])
    dup_roll = db_connection.get_filly_roll_id(dup_result['roll_data']['id'])

    assert dup_roll['id'] != original_roll['id'], "Duplicated roll should have a different ID"
    assert dup_roll['type_id'] == original_roll['type_id']
    assert dup_roll['brand_id'] == original_roll['brand_id']
    assert dup_roll['color_id'] == original_roll['color_id']
    assert dup_roll['subtype_id'] == original_roll['subtype_id']

    assert original_roll['original_weight_grams'] == 1000.0
    assert original_roll['weight_grams'] == 500.0
    assert dup_roll['original_weight_grams'] == 2000.0
    assert dup_roll['weight_grams'] == 2000.0

def test_change_in_use_status(db_connection):
    """Test the change_in_use_status method."""

    # this is dependent on insert_roll working in previous tests
    roll_id = 1
    roll_data = db_connection.get_filly_roll_id(roll_id)
    assert roll_data['in_use'] is False, "Initial in_use status should be False"
    result = db_connection.change_in_use_status(roll_id, True)
    assert result.get('result', False), "Change in_use status should be successful"
    assert result['roll_data']['in_use'] is True, "in_use status should be True after update"
    roll_data = db_connection.change_in_use_status(roll_id, False)
    assert roll_data.get('result', False), "Change in_use status should be successful"
    assert roll_data['roll_data']['in_use'] is False, "in_use status should be False after update"

def test_open_roll(db_connection):
    """Test the open_roll method."""

    # this is dependent on insert_roll working in previous tests
    roll_id = 2
    roll_data = db_connection.get_filly_roll_id(roll_id)
    assert roll_data['opened'] is False, "Initial opened status should be False"
    result = db_connection.open_roll(roll_id)
    assert result.get('result', False), "Open roll should be successful"
    assert result['roll_data']['opened'] is True, "Opened status should be True after opening the roll"
    roll_data = db_connection.get_filly_roll_id(roll_id)
    assert roll_data['opened'] is True, "Opened status should remain True"

def test_update_roll_weight(db_connection):
    """Test the update_roll_weight method."""
    # insert new roll for this test
    insert_result = db_connection.insert_roll(
        type_id=3,
        brand_id=3,
        color_id=3,
        subtype_id=3,
        original_weight_grams=1000.0,
        weight_grams=750.0,
        opened=False,
        in_use=False
    )
    assert insert_result.get('result', False), "Roll insertion should be successful"
    roll_id = insert_result['roll_data']['id']
    # test setting the weight
    update_result = db_connection.update_roll_weight(roll_id, 600.0)
    assert update_result.get('result', False), "Update roll weight should be successful"
    assert update_result['roll_data']['weight_grams'] == 600.0, "Roll weight should be updated correctly"
    roll_data = db_connection.get_filly_roll_id(roll_id)
    assert roll_data['weight_grams'] == 600.0, "Roll weight should reflect the updated value"
    # test decreasing weight
    update_result = db_connection.update_roll_weight(roll_id, None, decr_weight_grams=100.0)
    assert update_result.get('result', False), "Decrease roll weight should be successful"
    assert update_result['roll_data']['weight_grams'] == 500.0, "Roll weight should be decreased correctly"
    roll_data = db_connection.get_filly_roll_id(roll_id)
    assert roll_data['weight_grams'] == 500.0, "Roll weight should reflect the decreased value"

def test_get_filly_rolls_active_filter(db_connection):
    """Test the get_filly_rolls_active method with various filters."""
    # Insert 1 new roll that doesn't match any other tests
    insert_result = db_connection.insert_roll(
        type_id=1,
        brand_id=2,
        color_id=3,
        subtype_id=4,
        original_weight_grams=1000.0,
        weight_grams=800.0,
        opened=True,
        in_use=False
    )
    assert insert_result.get('result', False), "Roll insertion should be successful"
    # Test filtering by type_id and brand_id
    rolls = db_connection.get_filly_rolls_active_filter(type_id=1, brand_id=2)
    assert len(rolls) == 1, "There should only be 1 roll"
    # filter by type_id and color_id
    rolls = db_connection.get_filly_rolls_active_filter(type_id=1, color_id=3)
    assert len(rolls) == 1, "There should only be 1 roll"

def test_get_filly_rolls_all(db_connection):
    """Test the get_filly_rolls_all method with various filters."""
    # Test filtering by subtype_id
    rolls = db_connection.get_filly_rolls_all()
    assert len(rolls) >= 1, "There should be at least 1 roll with subtype_id 1"

    # test that all rolls have a type_id, brand_id, color_id, subtype_id
    for roll in rolls:
        assert 'type_id' in roll, "Roll should have type_id"
        assert 'brand_id' in roll, "Roll should have brand_id"
        assert 'color_id' in roll, "Roll should have color_id"
        assert 'subtype_id' in roll, "Roll should have subtype_id"

def test_get_filly_all_vs_filter(db_connection):

    all_rolls = db_connection.get_filly_rolls_all()
    filter_rolls = db_connection.get_filly_rolls_active_filter() # should get all above g weight

    for roll in filter_rolls:
        assert roll in all_rolls, "Filtered rolls should be a subset of all rolls"
    assert len(filter_rolls) <= len(all_rolls), "Filtered rolls should not exceed all rolls"