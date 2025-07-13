import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "",
)


def ai_request(prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
    completion = client.chat.completions.create(model="cntrlprod", messages=messages)

    return completion.choices[0].message.content


def llama_ai(prompt):
    endpoint = "https://api.together.xyz/v1/chat/completions"
    res = requests.post(
        endpoint,
        json={
            "model": "meta-llama/Llama-3-70b-chat-hf",
            "max_tokens": 8000,
            "temperature": 0.3,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": ["<|eot_id|>"],
            "messages": [{"content": prompt, "role": "user"}],
        },
        headers={
            "Authorization": f"Bearer {os.getenv('LLAMA_API_KEY')}",
        },
    )
    return res.json()["choices"][0]["message"]["content"]
