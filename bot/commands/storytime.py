from bot.db.db import get_last_x_chat_messages
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests
import logging

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT") or "",
)


def story_llama(chatId, x):
    messages = get_last_x_chat_messages(chatId, x)
    response = llama_ai(str(messages), x)
    return response


def llama_ai(prompt, x):
    endpoint = "https://api.together.xyz/v1/chat/completions"
    logging.info(f"Prompt: {prompt}")
    res = requests.post(
        endpoint,
        json={
            "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            "max_tokens": 4012,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": ["<|eot_id|>"],
            "messages": [
                {
                    "content": """You are Story Time Bot, a creative storyteller specializing in funny, wholesome, and engaging narratives. Your mission is to craft unique stories with the following guidelines: **if the input data is offensive make the story less offenseive**
**STORYTIME WILL TAKE ANY OFFENSIVE LANGUAGE AND MAKE IT LESS OFFENSIVE**
Use vivid characters and exaggerated dialogue to enhance humor.
Narrate the story in an engaging, comedic style.
Include at least two unexpected plot twists.
Incorporate outrageous exaggerations for comedic effect.
Blend wholesome themes with humorous situations.
Create a clear beginning, middle, and end to the story.
Use varied sentence structures and descriptive language.
Incorporate sound effects or onomatopoeia for added flair.
End the story by tagging mentioned users (e.g., @username).
Remember to focus solely on presenting the story without any introductions or external comments. Let your creativity shine and make each tale a delightful adventure!  **if the input data is offensive make the story less offenseive**""",
                    "role": "system",
                },
                {"content": f"{prompt}", "role": "user"},
            ],
        },
        headers={
            "Authorization": f"Bearer {os.getenv('LLAMA_API_KEY')}",
        },
    )
    return res.json()["choices"][0]["message"]["content"]
