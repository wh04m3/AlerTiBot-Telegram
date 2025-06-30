from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove,ReplyKeyboardMarkup
from telegram.ext import ContextTypes,ConversationHandler
from api import geocodificacion,clima
import logging


# /start
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔍 ¿Hay alguna alerta?", callback_data="alerta")],
        [InlineKeyboardButton("🌦 Clima por zona", callback_data="clima")],
        [InlineKeyboardButton("🧰 ¿Qué hacer en caso de riesgo?", callback_data="acciones")],
        [InlineKeyboardButton("📢 Reportar inundación", callback_data="reporte")],
        [InlineKeyboardButton("🚨 Emergencia", callback_data="emergencia")]
    ]
   # reply_markup = InlineKeyboardMarkup(keyboard)
    nombre = update.effective_user.first_name
    menu = [['🌧 Ver clima', 'ℹ️ Ayuda'], ['🚨 Alertas', '📍 Ubicación']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(f'👋 ¡Hola, {nombre}! Soy *AlerTiBot*, tu asistente de alertas en caso de inundacion del TESCHI.\n'
        '¿Qué deseas hacer?', reply_markup=reply_markup,parse_mode='Markdown')
    
    
    
UBI = range(2)
# /alerta
async def alerta_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Para buscar alertas en tu zona\nEnvíame tu ubicación actual tocando el clip 📎 o el botón 📍Ubicación\nO envia /cancelar para abortar")
    return UBI
    

async def ubicacion_alerta(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    #context.user_data["ubicacion"] = update.message.text
    #reply_keyboard = [["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"]]
    location = update.message.location
    lat = location.latitude
    lon = location.longitude
    direccion=geocodificacion.obtener_direccion(lat,lon)
    
    await update.message.reply_text(f"Estoy revisando los datos más recientes cerca de 🌧\nUbicacion:\n{direccion}\n🌐 Consulta el mapa de zonas afectadas aquí:\n👉 http://alertibot-map.sytes.net/", parse_mode="Markdown")
   
    return ConversationHandler.END 




# Al hacer clic en un botón del menú
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "alerta":
        await query.edit_message_text("Según el último reporte, hay una alerta de inundación moderada en tu zona.")
    elif query.data == "clima":
        await query.edit_message_text(clima.resumen_clima_actual())
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

    if "agua" in texto or "inundando" in texto or "inundando" in texto  or "reportar" in texto  or "reporte" in texto:
        await update.message.reply_text("Para empezar el reporte de una inundacion en el lugar donde te encuentras envia el comando /reporte")
    elif "hola" in texto or "buenas" in texto:
        await update.message.reply_text("¡Hola! ¿Necesitas saber sobre alertas o reportar una inundación?")
    elif "menu" in texto or "opciones" in texto:
        keyboard = [
        [InlineKeyboardButton("🔍 ¿Hay alguna alerta?", callback_data="alerta")],
        [InlineKeyboardButton("🌦 Clima por zona", callback_data="clima")],
        [InlineKeyboardButton("🧰 ¿Qué hacer en caso de riesgo?", callback_data="acciones")],
        [InlineKeyboardButton("📢 Reportar inundación", callback_data="reporte")],
        [InlineKeyboardButton("🚨 Emergencia", callback_data="emergencia")]
    ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
        nombre = update.effective_user.first_name
        menu = [['🌧 Ver clima', 'ℹ️ Ayuda'], ['🚨 Alertas', '📍 Ubicación']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

        await update.message.reply_text('¿Qué deseas hacer?', reply_markup=reply_markup,parse_mode='Markdown')
    elif "pronostico" in texto or "clima" in texto:
        await update.message.reply_text(clima.resumen_clima_actual())
    elif "alertas" in texto or "ver alertas" in texto or "alerta" in texto or "mostrar alertas" in texto:
        await update.message.reply_text("Si necesitas verificar si existe alguna alerta de inundacion envia /alertas?")
    elif "ayuda" in texto or "riesgo" in texto or "que hacer" in texto or "informacion" in texto:
        await update.message.reply_text(
    "🚨 ¿Qué hacer durante una inundación?\n\n"
    "• No camines por zonas inundadas.\n"
    "  Podrías caer en hoyos o coladeras abiertas o incluso el agua podria estar electrificada.\n\n"
    "• Evita puentes bajos, pasos a desnivel y túneles.\n"
    "  Se inundan muy rápido.\n\n"
    "• No uses transporte público si hay alerta de inundación.\n"
    "  Podría quedar atrapado.\n\n"
    "• Sigue instrucciones de protección civil o autoridades locales.\n\n"
    "• Si estás atrapado, busca un lugar alto y seguro.\n"
    "  No intentes cruzar corrientes fuertes.\n\n"
    "⚠️ ¡Tu seguridad es primero! Si ves agua acumulada, da la vuelta."
)
    elif "Adios" in texto or "bye" in texto or "hasta luego" in texto or "nos vemos" in texto:
        await update.message.reply_text("Gracias por tu mensaje. Si necesitas ayuda, puedes usar el menú o escribir una palabra clave como 'inundación'.")
    elif "emergencia" in texto or "auxilio" in texto:
        await update.message.reply_text(
    "🚨 ¿Qué hacer en caso de una emergencia?\n\n"
    "• Mantén la calma. Respira profundo y evita el pánico.\n\n"
    "• Llama al 911 o al número de emergencias local si es necesario.\n\n"
    "• Aléjate de zonas peligrosas como cables caídos, fuego o agua acumulada.\n\n"
    "• Si estás en un edificio, evacúa si es seguro hacerlo. Usa las escaleras, no el elevador.\n\n"
    "• Ayuda a niños, personas mayores o con discapacidad si puedes hacerlo sin ponerte en riesgo.\n\n"
    "• Sigue las indicaciones de las autoridades o equipos de emergencia.\n\n"
    "⚠️ Ten siempre a la mano un kit de emergencia con agua, linterna, radio, documentos y botiquín básico."
)
    else:
        await update.message.reply_text(f'No entendi tu mensaje, puedes intentar con una palabra clave como *Ayuda*, *Menu*, *Reporte*',parse_mode='Markdown')
        

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
#Flujo de reporte de inundacion
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Estados del flujo
UBICACION, GRAVEDAD,PHOTO, COMENTARIO = range(4)

# Inicio del flujo
async def iniciar_reporte(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Gracias por avisarnos! ¿En qué ubicación estás viendo la inundación?\n"
        "(Envíame tu ubicación actual tocando el clip 📎 o el botón 📍Ubicación)"
    )
    return UBICACION

# Paso 1: ubicación
async def recibir_ubicacion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    context.user_data["ubicacion"] = update.message.text
    reply_keyboard = [["Muy Bajo", "Bajo", "Medio", "Alto", "Muy Alto"]]
    await update.message.reply_text("Gracias. ¿Qué tan grave es la inundación?",
    reply_markup=ReplyKeyboardMarkup(
        reply_keyboard, one_time_keyboard=True, input_field_placeholder="Gravedad"
    ),
 )
    return GRAVEDAD

# Paso 2: gravedad
async def recibir_gravedad(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["gravedad"] = update.message.text
    user = update.message.from_user
    logger.info("Gravedad of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Estamos recibiendo tu reporte, por favor envia una fotografia del estado de la inundacion\nSi no deseas agregar fotgrafia envia /saltar",
        reply_markup=ReplyKeyboardRemove(),
    )
    return PHOTO

# Paso 3: comentario y cierre
async def recibir_comentario(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data["comentario"] = update.message.photo
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    #logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")

    # resumen = (
    #     f"📍 Ubicación: {context.user_data['ubicacion']}\n"
    #     f"🌊 Gravedad: {context.user_data['gravedad']}\n"
    #     #f"💬 Comentario: {context.user_data['comentario']}"
    # )

    await update.message.reply_text("✅ Tu reporte fue recibido:\nGracias por tu aporte, ayudas a que mas gente este prevenida sobre inundaciones en la zona\nSi puedes reportar otra inundacion aqui estare, cada aporte cuenta")
    return ConversationHandler.END

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    #logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "Gracias por tu aporte, ayudas a que mas gente este prevenida sobre inundaciones en la zona\nSi puedes reportar otra inundacion aqui estare, cada aporte cuenta\nPara la proxima puedes considerar enviar una fotografia para ayudar a tener un contexto mas claro de la situación "
    )


# Cancelación
async def cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operación cancelada.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END