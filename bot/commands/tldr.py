from db.db import get_last_x_chat_messages



def tldr(chatId, x):
    messages = get_last_x_chat_messages(chatId, x)
    return messages