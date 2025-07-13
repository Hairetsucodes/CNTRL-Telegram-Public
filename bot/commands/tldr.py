from db.db import get_last_x_chat_messages
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


def ai_request(prompt, x):
    messages = [
        {
            "role": "system",
            "content": f"The following is a log file of the last {x} messages in this chat, please provide a summary of the chat. a TLDR if you will.",
        },
        {"role": "user", "content": prompt},
    ]
    completion = client.chat.completions.create(model="cntrlprod", messages=messages)

    return completion.choices[0].message.content


def tldr(chatId, x):
    messages = get_last_x_chat_messages(chatId, x)
    response = ai_request(str(messages), x)
    print(f"AI response: {response}")
    return response


def tldr_llama(chatId, x):
    messages = get_last_x_chat_messages(chatId, x)
    print(f"Messages: {messages}")
    response = llama_ai(str(messages), x)
    print(f"AI response: {response}")
    return response


def llama_ai(prompt, x):
    endpoint = "https://api.together.xyz/v1/chat/completions"

    res = requests.post(
        endpoint,
        json={
            "model": "meta-llama/Llama-3-70b-chat-hf",
            "max_tokens": 512,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stop": ["<|eot_id|>"],
            "messages": [
                {
                    "content": f"<human>: Hi! <bot>: My name is TLDR Bot, I am a system for analying conversations and summarizing them.. In response to every request I will summarize the input logs into a detailed sweet tldr response The following is a log file of the last {x} messages in this chat, please provide a summary of the chat..",
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
