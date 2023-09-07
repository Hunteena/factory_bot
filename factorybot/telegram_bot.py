import logging
import os

import django
from django.conf import settings
from telegram import Update
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


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Для использования бота перейдите в Django API и выполните следующие действия:\n"
        "1) зарегистрируйтесь,\n"
        "2) авторизуйтесь,\n"
        "3) сгенерируйте токен и отправьте в этот чат.\n"
        "Теперь сообщения, отправленные через Django API, будут пересланы в этот чат"
    )


async def bind_chat(update: Update,
                    context: ContextTypes.DEFAULT_TYPE) -> None:
    """Bind chat to user if correct token was sent."""
    token = update.message.text
    try:
        user = await User.objects.aget(token=token)
        if user.chat_id:
            message = 'Токен уже подтвержден'
        else:
            user.chat_id = update.message.chat_id
            await user.asave()
            message = 'Токен подтвержден'
    except User.DoesNotExist:
        message = ('Неверный токен. '
                   'Получите токен подтверждения и отправьте его в этот чат')

    await update.message.reply_text(message)


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(
        settings.TELEGRAM_BOT_TOKEN
    ).build()

    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, bind_chat)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
