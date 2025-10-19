import os
from re import M
from dotenv import load_dotenv

load_dotenv()

import openai

model_name = os.getenv("MODEL_NAME")
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")


client = openai.OpenAI(
    base_url=base_url,
    api_key=api_key,
)

response = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ],
)

print(response.choices[0].message.content)