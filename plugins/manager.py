import importlib
import os

class PluginManager:
    def __init__(self, plugins_folder="plugins"):
        self.plugins_folder = plugins_folder
        self.plugins = {}

    def load_plugins(self):
        for file in os.listdir(self.plugins_folder):
            if file.endswith(".py") and file != "manager.py":
                name = file[:-3]
                module = importlib.import_module(f"plugins.{name}")
                self.plugins[name] = module

    def get_plugin(self, name):
        return self.plugins.get(name)
    
    def execute_plugin_step(step):
        from .plugin_runner import run_plugin
        plugin = step["plugin"]
        action = step["action"]
        args = step.get("args", {})
        return run_plugin(plugin, action, args)

plugin_manager = PluginManager()
plugin_manager.load_plugins()
