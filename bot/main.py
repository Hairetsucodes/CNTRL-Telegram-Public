import os
from dotenv import load_dotenv
import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from commands.ai import ai_request
from db.db import engine


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    print(user)
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        """
Welcome to CNTRL AI bot.
Here are a list of commands you can use:
/cntrl - Use this command to interact with the AI.
/help - Use this command to get help.
        """
    )


async def ai(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(set(update.message.text.strip('/cntrl '))) < 2:
        return await update.message.reply_text('I\'m sorry, I can\'t process empty messages.')
    print(update.message.text)
    temporary = await update.message.reply_text("Just a second! I am processing your request.")
    await update.message.delete()
    response = ai_request(update.message.text)
    await context.bot.deleteMessage(message_id=temporary.message_id,
                                    chat_id=update.message.chat_id)
    await update.message.reply_text(response)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)

def main() -> None:
    token = os.getenv("BOT_API_KEY")
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cntrl", ai))
    application.add_handler(MessageHandler(filters.Text & ~filters.Command, echo))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    load_dotenv()
    main()
