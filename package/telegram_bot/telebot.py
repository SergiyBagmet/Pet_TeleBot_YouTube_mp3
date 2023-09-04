from .API import TOKEN_API
from ..conversion.convert import ConvertYouTube

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, ConversationHandler, CallbackContext, Filters



def start(update: Update, context: CallbackContext) :
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text="Hi send me a link to music from youtube."
        )
  
def download_mp3(update: Update, context: CallbackContext) -> None:
    link = update.message.text
    try:
        yt = ConvertYouTube(link)
        context.bot.send_message(
        chat_id = update.effective_chat.id,
        text="Please wait loading."
        )
        yt.link_to_mp3_transaction()
        context.bot.send_audio(
            chat_id=update.message.chat_id, 
            audio = open(yt.path_mp3, "rb")
            )
    except ValueError:
        update.message.reply_text("Error.")
    
    


def run_telebot():
    updater = Updater(TOKEN_API, use_context=True)

    dispatcher = updater.dispatcher

    # Создайте обработчики команды /start и текстовых сообщений
    start_handler = CommandHandler('start', start)
    downlod_mp3_handler = MessageHandler(Filters.text & ~Filters.command, download_mp3)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(downlod_mp3_handler)

    # Запустите бота
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run_telebot()