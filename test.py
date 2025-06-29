from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

TOKEN = '7627891801:AAEoV04-jl0SDDIkHiqWKl2UpQRfv9l4QdA'

# Cuando el usuario escribe /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola 👋. Envíame tu ubicación actual tocando el clip 📎 o el botón 📍Ubicación.")

# Manejador de ubicaciones
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat = location.latitude
    lon = location.longitude
    await update.message.reply_text(f"Ubicacion:\nLat: {lat}\nLon: {lon}")
    
    # Aquí podrías llamar a una API de clima, zonas de riesgo, etc.

# Ejecutar bot
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))  # <- captura ubicación

    app.run_polling()
