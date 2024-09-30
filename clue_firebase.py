import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

num_of_itr = 3

client = OpenAI(api_key = os.environ.get("OPENAI_API_KEY"))

# Initialize the Firebase app with your service account credentials
cred = credentials.Certificate("tinfoil-22924-firebase-adminsdk-yoy3r-fd0074e406.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tinfoil-22924-default-rtdb.firebaseio.com/'
})
ref = db.reference('/clues/')

def get_clues():
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": """
You are to work on a political conspiracy creator game. The player is to be presented with a list of things like notes, news snippets, images and real world location markers. 
They can then connect them in any order with some relationship between the connections. This final conspiracy is to be judged and scored to rank the player on a global leaderboard.
                """.strip()
                }
            ]
            },
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": "Create 5 of each clue_type"
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

    data = json.loads(content)
    print(f"Data loaded: {data}")

    for idx, clue in enumerate(data["all_data"], start=0):
        clue_type = clue["clue_type"]
        clue_content = clue["clue_content"]
        print(f"Clue {idx+1}: {clue_type} - {clue_content}")
        
        if(clue_type.lower() == "image"):
            response = client.images.generate(
                model = "dall-e-2",
                prompt = clue_content,
                size = "256x256",
                n = 1,
                response_format = "b64_json"
            )
            # print(f"Image response: {response}")
            
            b64_json = response.data[0].b64_json
            clue["b64_json"] = b64_json
            print(f"Image b64_json: {b64_json[:10]}")

        # Push data to Firebase
        ref.push(clue)

    print(f"Data written successfully!")