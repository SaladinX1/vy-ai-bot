from vision.screen_capture import take_screenshot
from vision.ocr import extract_text
from llm.llm_interface import get_command_response
import json
from vision.detect_and_click import click_on_text
from execution.keyboard_control import type_text
from execution.app_launcher import open_app
from agents.run_loop import run_agent
from agents.planner import AgentPlanner

def main():
    agent = AgentPlanner()
    while True:
        user_input = input("\n💬 Que veux-tu faire ? (exit pour quitter) >>> ")
        if user_input.lower() == "exit":
            break
        agent.run(user_input)

if __name__ == "__main__":
    main()
