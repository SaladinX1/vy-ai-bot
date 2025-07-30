import pytest
from core.planner_agent import AgentPlanner

def test_generate_plan_valid():
    planner = AgentPlanner()
    plan = planner.generate_plan("Créer un blog sur l'IA")
    assert isinstance(plan, list)
    if plan:
        assert "id" in plan[0]
        assert "title" in plan[0]
        assert "depends_on" in plan[0]
