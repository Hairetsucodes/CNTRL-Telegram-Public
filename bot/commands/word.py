from db.db import word_results



def lastYT(chatId, userId):
    results = word_results(chatId, userId)
    return results