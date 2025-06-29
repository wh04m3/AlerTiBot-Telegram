def start_handler(update, context):
    update.message.reply_text("¡Bienvenido! Usa /alerta para ver riesgos de inundación.")

def alerta_handler(update, context):
    zona = "Oaxaca"  # puedes extraer del usuario
    mensaje = verificar_alerta(zona)  # vendría de tu lógica
    update.message.reply_text(mensaje)
