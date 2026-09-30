import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

os.getenv("GROQ_API_KEY")

def generate_response(
    api_key,
    model,
    messages,
    max_tokens=4096
):
    client = Groq(
        api_key=api_key
    )

    params = {
        "model": model,
        "messages": messages,
    }

    if max_tokens:
        params["max_tokens"] = max_tokens

    response = client.chat.completions.create(**params)

    return response.choices[0].message.content