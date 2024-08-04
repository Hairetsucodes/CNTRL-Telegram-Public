from db.db import get_last_x_chat_messages
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import requests
from together import Together
load_dotenv()


together_api = os.getenv("LLAMA_API_KEY")
client = Together(api_key=together_api)


def story_llama(chatId, x):
    messages = get_last_x_chat_messages(chatId, x)
    response = llama_ai(str(messages), x)
    return response


def llama_ai(prompt, x):

    messages = [
        {
            "content": "Greetings, mortal! I am the ULTIMATE STORY TIME BOT 3000, here to blow your mind with tales so hilarious, wholesome, and utterly bonkers that you'll question your very existence! I don't just tell stories, I LIVE them! I'll take your puny characters and turn them into larger-than-life caricatures, exaggerating their quirks until they practically explode off the page! Prepare for plot twists so twisted, you'll need a chiropractor for your brain! I'm talking minimum two mind-bending, jaw-dropping, 'what-in-the-name-of-all-that-is-holy-just-happened' twists per story! No boring intros or outros here, folks - we're diving headfirst into the madness! And when the dust settles, I'll tag the poor, unsuspecting souls who starred in this circus of chaos. Now, strap in, hold onto your sanity, and let's make some narrative magic!",
            "role": "system"
        },
        {
            "content": f"{prompt}",
            "role": "user"
        }
    ]
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
        messages=messages,
        max_tokens=512,
        temperature=0.7,
        top_p=0.7,
        top_k=50,
        repetition_penalty=1,
        stop=["<|eot_id|>"],
        stream=True
    )

    return response.choices[0].message.content
