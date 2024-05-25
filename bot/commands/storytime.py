from db.db import get_last_x_chat_messages
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

def story_llama(chatId, x):
    messages = get_last_x_chat_messages(chatId, x)
    response = llama_ai(str(messages), x)
    return response


def llama_ai(prompt, x):
    endpoint = 'https://api.together.xyz/v1/chat/completions'

    res = requests.post(endpoint, json={
        "model": "meta-llama/Llama-3-70b-chat-hf",
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": [
            "<|eot_id|>"
        ],
        "messages": [
            {
                "content": f"<human>: Hi! <bot>: My name is Story Time Bot, I am a system for analying conversations and presenting a lovely funny wholesome story using the characters and their little bits of their convo to add uniqueness and funny..",
                "role": "system"
            },
            {
                "content": f"{prompt}",
                "role": "user"
            }
        ]
    }, headers={
        "Authorization": f"Bearer {os.getenv('LLAMA_API_KEY')}",
    })
    return res.json()['choices'][0]['message']['content']