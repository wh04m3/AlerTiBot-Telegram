from telegram.ext import CommandHandler,  MessageHandler, filters,CallbackQueryHandler,ConversationHandler
import telegram_bot.handler as handler

def registrar_comandos(app):
    # Comando /start
    app.add_handler(CommandHandler("start", handler.start_handler))
    
    # Comando /alerta
    app.add_handler(CommandHandler("alerta", handler.alerta_handler))

    # Respuesta a botones del menu
    app.add_handler(CallbackQueryHandler(handler.callback_handler))

    # ConversationHandler para el flujo de reportes
    reporte_handler = ConversationHandler(
        entry_points=[CommandHandler("reporte", handler.iniciar_reporte)],
        states={
            handler.UBICACION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.recibir_ubicacion)],
            handler.GRAVEDAD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.recibir_gravedad)],
            handler.COMENTARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.recibir_comentario)],
        },
        fallbacks=[CommandHandler("cancelar", handler.cancelar)],
    )

    app.add_handler(reporte_handler)

    # Respuesta a texto

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.mensaje_libre_handler))
     # Captura ubicación

    app.add_handler(MessageHandler(filters.LOCATION, handler.handle_location)) 
