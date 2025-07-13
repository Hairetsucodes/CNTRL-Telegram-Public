import os
from dotenv import load_dotenv
import logging
import re
import itertools
import datetime
from collections import deque
from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from bot.commands.ai import ai_request
from bot.db.db import add_message
from bot.commands.yt import lastYT
from bot.commands.word import words
from bot.commands.tldr import tldr, tldr_llama
from bot.commands.storytime import story_llama
from bot.commands.gold import gold_price
from bot.commands.oil import oil_price
from bot.commands.ai import llama_ai
from bot.db.db import top_five_leaderboard
from bot.db.db import check_b7
from bot.db.db import last_five_messages
from bot.commands.helpme import helpme

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    await update.message.reply_text(
        """
Welcome to CNTRL AI bot.
Here are a list of commands you can use:
/ai - Use this command to interact with the AI.
/yt - Use this command to get the last youtube link pasted in chat.
/word - Use this command to get user word count.
/tldr - Use this command to get a summary of the chat.
/gold - Use this command to get the current gold price.
/oil - Use this command to get the current oil price.
/tldrllama - Use this command to get a summary of the chat using llama AI.
/dramallama - Use this command to get a summary of the chat using llama AI.
/helpme - Use this command to get help with management advice.
    /cntrlhelp - Use this command to get help.

        """
    )


async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )
    response = lastYT(update.message.chat_id)
    await update.message.reply_text(response)


async def oil(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )
    current_oil_price = oil_price()
    response = f""" The current price of crude is: ${current_oil_price}"""
    await update.message.reply_text(response)


async def gold(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )
    current_gold_price = gold_price()
    response = f""" The current gold price is: ${current_gold_price}"""
    await update.message.reply_text(response)


async def word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )
    wordScore = words(update.message.chat_id, update.effective_user.id)
    response = f""" {wordScore} """
    await update.message.reply_text(response)


async def top_five(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message:
        return
    results = top_five_leaderboard(update.message.chat_id)
    logging.info(f"Top five results: {results}")

    if not results:
        await update.message.reply_text("No results found.")
        return

    leaderboard = []
    for word, user_counts in results.items():
        formatted_users = [f"{user} - {count}" for user, count in user_counts.items()]

        leaderboard.append(
            f"🏆 Leaderboard:\n\nWord: {word}\n"
            + "\n".join([f"{i+1}. {entry}" for i, entry in enumerate(formatted_users)])
        )

    response = "\n\n".join(leaderboard)
    await update.message.reply_text(response)


async def tldr_ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )

    if update.message.text is None:
        await update.message.reply_text("No message text found.")
        return
    numbers = re.findall(r"\d+", update.message.text)

    numbers = [int(num) for num in numbers]

    if not numbers:
        response = "No numbers found in your message."
        await update.message.reply_text(response)
        return

    return_x = numbers[0]
    print(f"Return x: {return_x}")

    tldr_response = tldr(update.message.chat_id, return_x)

    response = f"{tldr_response}"

    await update.message.reply_text(response)


async def llama_tldr(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )

    if update.message.text is None:
        await update.message.reply_text("No message text found.")
        return
    numbers = re.findall(r"\d+", update.message.text)

    numbers = [int(num) for num in numbers]

    if not numbers:
        response = "No numbers found in your message."
        await update.message.reply_text(response)
        return

    return_x = numbers[0]
    print(f"Return x: {return_x}")

    tldr_response = tldr_llama(update.message.chat_id, return_x)

    response = f"{tldr_response}"

    await update.message.reply_text(response)


async def storytime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )

    tldr_response = story_llama(update.message.chat_id, 20)

    response = f"{tldr_response}"

    await update.message.reply_text(response)


async def llama(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    messages = last_five_messages(update.message.chat_id, update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )
    if not update.message.text or len(set(update.message.text.strip("/ai "))) < 2:
        await update.message.reply_text("I'm sorry, I can't process empty messages.")
        return
    response = llama_ai(update.message.text.strip("/llama "))
    await update.message.reply_text(response)
    logger.info(f"AI response: {response}")


async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"AI command received from: {update.effective_user.username} => {update.message.text}"
    )
    if not update.message.text or len(set(update.message.text.strip("/ai "))) < 2:
        await update.message.reply_text("I'm sorry, I can't process empty messages.")
        return
    response = ai_request(update.message.text.strip("/ai "))
    if response:
        await update.message.reply_text(response)
        logger.info(f"AI response: {response}")


async def chat_logging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message or not update.message.text:
        return

    username = update.effective_user.username or update.effective_user.first_name
    logger.info(f"full user info: {username}")
    now = datetime.datetime.now()

    # Convert to lowercase and remove words that repeat within the last 15 words
    original_message = (
        update.message.text.lower()
    )  # Convert entire message to lowercase
    words = original_message.split()
    cleaned_words = []
    recent_words = deque(maxlen=15)

    for word in words:
        if word not in recent_words:
            cleaned_words.append(word)
        recent_words.append(word)

    cleaned_message = " ".join(cleaned_words)

    add_message(
        id=update.effective_user.id,
        chatId=update.message.chat_id,
        username=username,
        message=cleaned_message,
    )

    if (
        update.effective_user.username and cleaned_message != "none"
    ):  # Changed "None" to "none"
        logger.info(f"full user info: {update.effective_user}")
        logger.info(
            f"User {update.effective_user.username} sent a message: {cleaned_message}"
        )
    else:
        logger.info(
            f"User {update.effective_user.id} sent a message: {cleaned_message}"
        )


async def helpme_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return
    user_check = check_b7(update.effective_user.id)
    if user_check:
        response = "I'm sorry, but due to the consensus of the chat, you are not authorized to use this command."
        await update.message.reply_text(response)
        return
    logger.info(
        f"Helpme command received from: {update.effective_user.username} => {update.message.text}"
    )

    helpme_response = helpme(update.message.chat_id)

    response = f"{helpme_response}"

    await update.message.reply_text(response)


def main() -> None:
    token = os.getenv("BOT_API_KEY")
    if not token:
        raise ValueError("BOT_API_KEY environment variable is required")

    from bot.db.db import create_tables

    create_tables()
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("cntrlhelp", help_command))
    application.add_handler(CommandHandler("ai", ai))
    application.add_handler(CommandHandler("llama", llama))
    application.add_handler(CommandHandler("tldrllama", llama_tldr))
    application.add_handler(CommandHandler("dramallama", llama_tldr))
    application.add_handler(CommandHandler("yt", youtube))
    application.add_handler(CommandHandler("word", word))
    application.add_handler(CommandHandler("top", top_five))
    application.add_handler(CommandHandler("storytime", storytime))
    application.add_handler(CommandHandler("oil", oil))
    application.add_handler(CommandHandler("gold", gold))
    application.add_handler(CommandHandler("tldr", tldr_ai))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, chat_logging)
    )

    application.add_handler(CommandHandler("helpme", helpme_command))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    load_dotenv()
    main()
