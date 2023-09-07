import logging
import os

import django
from asgiref.sync import sync_to_async
from django.conf import settings
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, \
    ContextTypes

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'factorybot.settings')
django.setup()

from api.models import User

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def bind_chat(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bind chat to user if correct token was sent."""
    message = 'Oops'
    token = update.message.text
    print(token)
    try:
        user = await sync_to_async(User.objects.get)(token=token)
        user.chat_id = update.message.chat_id
        user.save()
        message = 'Токен подтвержден'
    except User.DoesNotExist:
        message = ('Неверный токен. '
                   'Получите токен подтверждения и отправьте его в этот чат')

    await update.message.reply_text(message)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - bind_chat the message on Telegram
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bind_chat))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
