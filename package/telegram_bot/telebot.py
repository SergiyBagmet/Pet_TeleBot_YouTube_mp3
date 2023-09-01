from API import TOKEN_API

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters



def start(update: Update, context: CallbackContext) :
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text="Привет! Я зеркальный бот. Просто отправь мне сообщение, и я повторю его."
        )
  
def mirror(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    update.message.reply_text(f"Ты сказал: {user_input}")


def telegram_bot():
    updater = Updater(TOKEN_API, use_context=True)

    dispatcher = updater.dispatcher

    # Создайте обработчики команды /start и текстовых сообщений
    start_handler = CommandHandler('start', start)
    mirror_handler = MessageHandler(Filters.text & ~Filters.command, mirror)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(mirror_handler)

    # Запустите бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    telegram_bot()