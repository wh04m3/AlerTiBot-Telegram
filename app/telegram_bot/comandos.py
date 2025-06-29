from telegram.ext import CommandHandler
from app.telegram_bot.handlers import start_handler, alerta_handler

def registrar_comandos(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CommandHandler("alerta", alerta_handler))
