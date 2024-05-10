from db.db import get_last_x_chat_messages
import os
from openai import AzureOpenAI
from dotenv import load_dotenv


load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    api_version="2023-12-01-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def ai_request(prompt, x):
    messages = [
        {"role": "system", "content": f"The following is a log file of the last {x} messages in this chat, please provide a summary of the chat. a TLDR if you will."},
        {"role": "user", "content": prompt},
    ]
    completion = client.chat.completions.create(
        model="cntrlprod",
        messages=messages
    )

    return completion.choices[0].message.content

def tldr(chatId, x):
    messages = get_last_x_chat_messages(chatId, x)
    response = ai_request(messages, x)
    print(f"AI response: {response}")
    return response