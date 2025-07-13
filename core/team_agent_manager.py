# core/team_agent_manager.py

from core.agent import AutonomousAgent

class TeamAgentManager:
    def __init__(self):
        self.agents = {
            "seo": AutonomousAgent("SEO"),
            "content": AutonomousAgent("Content"),
            "dev": AutonomousAgent("Developer"),
            "sales": AutonomousAgent("Sales")
        }

    def assign_and_run(self, goal):
        results = {}
        for role, agent in self.agents.items():
            task = f"{goal} – rôle : {role}"
            result = agent.run_cycle(task)
            results[role] = result
        return results
