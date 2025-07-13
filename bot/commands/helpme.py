from bot.db.db import get_last_x_chat_messages
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


def helpme_ai_request(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are an expert management consultant and leadership coach. Analyze the following chat conversation between a manager and their employees. Based on the last 5 messages, provide specific, actionable advice on how to best handle the situation, motivate the employees, and get them to perform their job effectively. Focus on practical management strategies, communication techniques, and leadership approaches that will yield results.",
        },
        {"role": "user", "content": prompt},
    ]
    completion = client.chat.completions.create(model="cntrlprod", messages=messages)

    return completion.choices[0].message.content


def helpme(chatId):
    """
    Analyzes the last 5 messages in the chat and provides management suggestions
    on how to best handle employees and get them to do their job effectively.
    """
    messages = get_last_x_chat_messages(chatId, 5)
    response = helpme_ai_request(str(messages))
    print(f"Management advice: {response}")
    return response


def helpme_llama(chatId):
    """
    Analyzes the last 5 messages using Llama AI and provides management suggestions
    on how to best handle employees and get them to do their job effectively.
    """
    messages = get_last_x_chat_messages(chatId, 5)
    print(f"Messages: {messages}")
    response = llama_helpme_ai(str(messages))
    print(f"Management advice: {response}")
    return response


def llama_helpme_ai(prompt):
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
                    "content": "You are an expert management consultant and leadership coach. Your job is to analyze workplace conversations and provide actionable management advice. Focus on practical strategies to motivate employees, improve performance, resolve conflicts, and achieve business objectives. Always provide specific, implementable recommendations.",
                    "role": "system",
                },
                {
                    "content": f"Based on these recent chat messages between a manager and employees, provide specific management advice on how to best handle the situation and get the employees to perform their job effectively: {prompt}",
                    "role": "user",
                },
            ],
        },
        headers={
            "Authorization": f"Bearer {os.getenv('LLAMA_API_KEY')}",
        },
    )
    return res.json()["choices"][0]["message"]["content"]
