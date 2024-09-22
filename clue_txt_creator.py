from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

num_of_itr = 3
client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

def get_clues():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": "You are to work on a fun and absurd conspiracy creator game. The player is to be presented with a list of things like notes, news snippets, images and location markers. They can then connect them in any order with some relationship between the connections. This final conspiracy is to be judged and scored to rank the player on a global leaderboard."
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Create 1 of each clue_type"
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
            "type": "json_schema",
            "json_schema": {
            "name": "clue_data",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                "all_data": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "clue_type": {
                        "type": "string"
                        },
                        "clue_content": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "clue_type",
                        "clue_content"
                    ],
                    "additionalProperties": False
                    }
                }
                },
                "additionalProperties": False,
                "required": [
                "all_data"
                ]
            }
            }
        }
    )
    print(response)

    content = response.choices[0].message.content
    return content

for i in range(num_of_itr):
    content = get_clues()

    # Load the JSON data
    data = json.loads(content)

    # Get the current timestamp
    timestamp = datetime.now().strftime("%M%S")

    # Iterate through each clue and write to a text file
    for idx, clue in enumerate(data["all_data"], start=1):
        clue_type = clue["clue_type"]
        clue_content = clue["clue_content"]
        
        # Generate file name based on clue type and index
        file_name = f"./content/{idx}_{timestamp}_clue_{clue_type.strip()}.txt"
        
        # Write clue content to the file
        with open(file_name, 'w') as file:
            file.write(clue_content)

        print(f"Written clue to {file_name}")