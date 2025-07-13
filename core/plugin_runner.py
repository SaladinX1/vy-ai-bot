import importlib
import json
import os

from core import plan_executor
from workflows import manager

PLUGIN_DIR = "plugins"


def run_plugin(plugin_name, action, context={}):
    try:
        module_path = f"{PLUGIN_DIR}.{plugin_name}"
        plugin = importlib.import_module(module_path)
        if hasattr(plugin, "run"):
            return plugin.run(action, context)
        else:
            raise Exception(f"Plugin {plugin_name} n'a pas de fonction run()")
    except Exception as e:
        print(f"❌ Erreur plugin {plugin_name}: {e}")
        return None


def run_workflow(name):
    steps = manager.load_workflow(name)
    if not steps:
        print(f"❌ Workflow '{name}' introuvable")
        return

    context = {}
    print(f"▶️ Lancement de '{name}' - {len(steps)} étapes")

    for i, step in enumerate(steps):
        print(f"➡️ Étape {i + 1}: {step}")
        if isinstance(step, dict) and "plugin" in step:
            plugin_name = step["plugin"]
            action = step.get("action", {})
            run_plugin(plugin_name, action, context)
        else:
            plan_executor.execute_plan([step], context)

    print(f"✔️ Workflow '{name}' terminé")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python plugin_runner.py <workflow_name>")
    else:
        run_workflow(sys.argv[1])
