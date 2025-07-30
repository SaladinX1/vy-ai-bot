from core.orchestrator import BusinessOrchestrator

def test_orchestrator_run_all():
    plan = [
        {"id": "niche_analysis", "title": "Analyse de niche", "input": {"topic": "IA"}},
        {"id": "copywriting", "title": "Rédaction", "input": {"product": "SaaS"}},
    ]
    orchestrator = BusinessOrchestrator(plan)
    results = [orchestrator.execute_task(t) for t in plan]
    assert all(results)
