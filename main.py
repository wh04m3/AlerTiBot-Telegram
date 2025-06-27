from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# === CONFIGURACIÓN ===
TOKEN = '7627891801:AAEoV04-jl0SDDIkHiqWKl2UpQRfv9l4QdA'  # Reemplaza con tu token

# === COMANDOS ===

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombre = update.effective_user.first_name
    menu = [['🌧 Ver clima', 'ℹ️ Ayuda'], ['🚨 Alertas', '📍 Ubicación']]
    reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)

    await update.message.reply_text(
        f'👋 ¡Hola, {nombre}! Soy *AlerTiBot*, tu asistente de alertas del TESCHI.\n'
        '¿Qué deseas hacer?',
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📌 *Comandos disponibles:*\n'
        '/start - Inicia el bot\n'
        '/help - Muestra esta ayuda\n'
        'Escribe palabras clave como "clima", "alerta" o "ubicación" para más info.',
        parse_mode='Markdown'
    )

# === RESPUESTAS A MENSAJES ===

async def responder_mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if 'clima' in texto:
        await update.message.reply_text('🌦️ El clima actual es soleado con posibilidades de lluvia por la tarde.')
    elif 'alerta' in texto:
        await update.message.reply_text('🚨 Actualmente no hay alertas de inundación en tu zona.')
    elif 'ubicación' in texto:
        await update.message.reply_text('📍 Estás registrado en Chicoloapan, zona TESCHI.')
    else:
        await update.message.reply_text('🤖 No entendí tu mensaje. Usa el menú o escribe /help.')

# === MAIN ===

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    # Respuestas a texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder_mensajes))

    print("🤖 Bot en ejecución...")
    app.run_polling()

if __name__ == '__main__':
    main()
