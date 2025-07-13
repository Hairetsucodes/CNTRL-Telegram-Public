from db.db import last_youtube


def lastYT(chatId):
    youtube = last_youtube(chatId)
    return youtube
