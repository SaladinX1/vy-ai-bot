import pytest
from core import plan_executor

def test_click_without_target():
    action = plan_executor.Action("click")
    try:
        action.execute()
    except Exception:
        pytest.fail("Click sans target ne doit pas lever d'exception")

def test_type_without_value():
    action = plan_executor.Action("type")
    with pytest.raises(ValueError):
        action.execute()

def test_invalid_action():
    action = plan_executor.Action("invalid_action")
    with pytest.raises(ValueError):
        action.execute()
