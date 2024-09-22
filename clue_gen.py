from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": """
    You are to work on a fun and absurd conspiracy creator game. 
    The player is to be presented with a list of things like notes, news snippets, images and location markers. 
    They can then connect them in any order with some relationship between the connections.
    This final conspiracy is to be judged and scored to rank the player on a global leaderboard.
    """.strip()
            }
        ]
        },
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "Create 5 of each clue type"
            }
        ]
        }
    ],
    temperature=1,
    max_tokens=2048,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    response_format={
        "type": "text"
    }
)

content = response.choices[0].message.content
print(f"content\n{content}")