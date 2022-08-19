import pytest
import sys
sys.path.append("../../BELAZ_API")
sys.path.append("../../BELAZ_API/core")
from core.database_controller import DatabaseController
from core.parser import LineupParser

@pytest.fixture
def create():
    db_controller = DatabaseController()
    parser = LineupParser(db_controller)
    return db_controller, parser

'''
def test_db_controller_without_elements(create):
    db_controller, parser = create

    assert db_controller.get_all_items() == []

    assert db_controller.get_model(0) is None
    with pytest.raises(TypeError):
        assert db_controller.get_model("a") is None
    with pytest.raises(TypeError):
        assert db_controller.get_model(None) is None
    with pytest.raises(TypeError):
        assert db_controller.get_model() is None
    with pytest.raises(TypeError):
        assert db_controller.get_model(0.1) is None
    assert db_controller.get_model(1000000000000) is None
    with pytest.raises(TypeError):
        assert db_controller.get_model([]) is None

    assert db_controller.erase_lineup() is None

    assert db_controller.delete_model(0, None) == "Model is not found"
    assert db_controller.delete_model(None, None) == "Model is not found"
    assert db_controller.delete_model(0, None) == "Model is not found"
    assert db_controller.delete_model("0", "") == "Model is not found"
    assert db_controller.delete_model(0.01, None) == "Model is not found"

    assert db_controller.delete_series(0, None) is None
    assert db_controller.delete_series(None, None) is None
    assert db_controller.delete_series(0, None) is None
    assert db_controller.delete_series("0", "") is None
    assert db_controller.delete_series(0.01, None) is None
'''
