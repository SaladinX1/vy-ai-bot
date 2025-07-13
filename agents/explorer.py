# agents/explorer.py

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

def generate_business_opportunities(prompt="Quelles niches digitales sont prometteuses ?"):
    client = MistralClient(api_key="YOUR_API_KEY")
    response = client.chat(
        model="mistral-tiny",
        messages=[ChatMessage(role="user", content=prompt)]
    )
    ideas = response.choices[0].message.content
    return [idea.strip("- ") for idea in ideas.split("\n") if idea.startswith("- ")]
