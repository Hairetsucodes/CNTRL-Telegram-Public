import os
from dotenv import load_dotenv
import logging

import datetime

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from commands.ai import ai_request
from db.db import engine, add_message
from commands.yt import lastYT
from commands.word import words


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)



async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
Welcome to CNTRL AI bot.
Here are a list of commands you can use:
/ai - Use this command to interact with the AI.
/yt - Use this command to get the last youtube link pasted in chat.
/help - Use this command to get help.

        """
    )

async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"AI command received from: {update.effective_user.username} => {update.message.text}")
    response = lastYT(update.message.chat_id)
    await update.message.reply_text(response)

async def word(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"AI command received from: {update.effective_user.username} => {update.message.text}")
    wordScore = words(update.message.chat_id, update.effective_user.id)
    response = f""" {wordScore} """
    await update.message.reply_text(response)




async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(f"AI command received from: {update.effective_user.username} => {update.message.text}")
    if len(set(update.message.text.strip('/ai '))) < 2:
        return await update.message.reply_text('I\'m sorry, I can\'t process empty messages.')
    response = ai_request(update.message.text)
    await update.message.reply_text(response)
    logger.info(f"AI response: {response}")


async def chat_logging(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    now = datetime.datetime.now()
    """ sanitize the input and log the message"""
    add_message(id=update.effective_user.id, chatId=update.message.chat_id, username=update.effective_user.username,  message=update.message.text)
    if update.effective_user.username and update.message.text != "None":
        logger.info(f"full user info: {update.effective_user}")
        logger.info(f"User {update.effective_user.username} sent a message: {update.message.text}")
    else:
        logger.info(f"User {update.effective_user.id} sent a message:")



def main() -> None:
    token = os.getenv("BOT_API_KEY")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("ai", ai))
    application.add_handler(CommandHandler("yt", youtube))
    application.add_handler(CommandHandler("word", word))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_logging))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    load_dotenv()
    main()
