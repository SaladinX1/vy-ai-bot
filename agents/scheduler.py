# agents/scheduler.py

import schedule
import time
from core.ideator import Ideator
from core.workflow_generator import WorkflowGenerator
from core.publisher import Publisher
from core.improver import Improver

ideator = Ideator()
workflow = WorkflowGenerator()
publisher = Publisher()
improver = Improver()

def daily_autorun():
    idea = ideator.generate_idea()
    plan = workflow.generate_plan(idea)

    publisher.publish_product_gumroad({"name": idea, "description": "Produit généré automatiquement"})
    publisher.tweet(f"Nouveau produit lancé: {idea}")

    improver.analyze_and_improve()

def run_scheduler():
    schedule.every().day.at("10:00").do(daily_autorun)
    while True:
        schedule.run_pending()
        time.sleep(60)
