from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove,ReplyKeyboardMarkup
from telegram.ext import ContextTypes,ConversationHandler
from api import geocodificacion

# /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 ¿Hay alguna alerta?", callback_data="alerta")],
        [InlineKeyboardButton("🌦 Clima por zona", callback_data="clima")],
        [InlineKeyboardButton("🧰 ¿Qué hacer?", callback_data="acciones")],
        [InlineKeyboardButton("📢 Reportar inundación", callback_data="reporte")],
        [InlineKeyboardButton("🚨 Emergencia", callback_data="emergencia")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    nombre = update.effective_user.first_name
    menu = [['🌧 Ver clima', 'ℹ️ Ayuda'], ['🚨 Alertas', '📍 Ubicación']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text("¿En qué puedo ayudarte hoy?", reply_markup=reply_markup)

# /alerta
async def alerta_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Estoy revisando los datos más recientes… 🌧")


# Al hacer clic en un botón del menú
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "alerta":
        await query.edit_message_text("Según el último reporte, hay una alerta de inundación moderada en tu zona.")
    elif query.data == "clima":
        await query.edit_message_text("Se han reportado lluvias intensas en las últimas horas.")
    elif query.data == "acciones":
        await query.edit_message_text(
            "✅ Antes: Ten documentos, lámpara y botiquín.\n"
            "⚠ Durante: Evita zonas bajas y escucha noticias.\n"
            "🧹 Después: No entres a casas dañadas. Llama a Protección Civil."
        )
    elif query.data == "reporte":
        await query.edit_message_text("Por favor, comparte tu ubicación o escribe tu colonia para reportar.")
    elif query.data == "emergencia":
        await query.edit_message_text("🚨 Llama al 911 o a Protección Civil y sube a un lugar seguro.")
    else:
        await query.edit_message_text("Opción no reconocida.")
#Respuesta a texto 
async def mensaje_libre_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()

    if "inundación" in texto or "inundacion" in texto or "agua" in texto or "inundando" in texto or "inundando" in texto:
        await update.message.reply_text("¿Puedes compartir tu ubicación o describir la zona afectada?")
    elif "hola" in texto or "buenas" in texto:
        await update.message.reply_text("¡Hola! ¿Necesitas saber sobre alertas o reportar una inundación?")
    elif "informacion" in texto or "hacer en caso de inundacion" in texto:
        await update.message.reply_text("¡Hola! ¿Necesitas saber sobre alertas o reportar una inundación?")
    else:
        await update.message.reply_text("Gracias por tu mensaje. Si necesitas ayuda, puedes usar el menú o escribir una palabra clave como 'inundación'.")

#Responder a ubicacion
async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.location
    lat = location.latitude
    lon = location.longitude
    direccion=geocodificacion.obtener_direccion(lat,lon)
    direccion2=geocodificacion.obtener_municipio(lat,lon)
    direccion3=geocodificacion.obtener_direccion_clave(lat,lon)
    await update.message.reply_text(f"Ubicacion:\nLat: {lat}\nLon: {lon} \ndireccion:{direccion}\ndireccion2:{direccion2}\ndireccion clave {direccion3}")
    return (lat,lon)



# Estados del flujo
UBICACION, GRAVEDAD, COMENTARIO = range(3)

# Inicio del flujo
async def iniciar_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Gracias por avisarnos! ¿En qué ubicación estás viendo la inundación?\n"
        "(Escribe colonia, ciudad o dirección exacta)"
    )
    return UBICACION

# Paso 1: ubicación
async def recibir_ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ubicacion"] = update.message.text
    await update.message.reply_text("Gracias. ¿Qué tan grave es la inundación?")
    return GRAVEDAD

# Paso 2: gravedad
async def recibir_gravedad(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["gravedad"] = update.message.text
    await update.message.reply_text("¿Deseas agregar algún comentario adicional?")
    return COMENTARIO

# Paso 3: comentario y cierre
async def recibir_comentario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["comentario"] = update.message.text

    resumen = (
        f"📍 Ubicación: {context.user_data['ubicacion']}\n"
        f"🌊 Gravedad: {context.user_data['gravedad']}\n"
        f"💬 Comentario: {context.user_data['comentario']}"
    )

    await update.message.reply_text("✅ Tu reporte fue recibido:\n" + resumen)
    return ConversationHandler.END

# Cancelación
async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operación cancelada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END