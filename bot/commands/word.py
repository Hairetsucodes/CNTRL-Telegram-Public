from db.db import word_results


def words(chatId, userId):
    results = word_results(chatId, userId)
    return results
