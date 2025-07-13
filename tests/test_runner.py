def test_runner_executes():
    from workflows.runner import run_workflow
    assert run_workflow("seo_webstarter") is None