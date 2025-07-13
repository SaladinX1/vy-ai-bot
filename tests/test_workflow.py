from workflows import manager
from workflows.manager import validate_workflow
import pytest

def test_save_load():
    workflow = [{"action": "click", "target": "Paramètres", "value": None}]
    manager.save_workflow("test", workflow)
    loaded = manager.load_workflow("test")
    assert loaded == workflow



def test_workflow_validation():
    valid_steps = [{"action": "do_something"}]
    assert validate_workflow(valid_steps) == True

    invalid_steps = [{}]
    with pytest.raises(ValueError):
        validate_workflow(invalid_steps)
