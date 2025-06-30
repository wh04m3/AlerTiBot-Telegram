from telegram.ext import CommandHandler,  MessageHandler, filters,CallbackQueryHandler,ConversationHandler
import telegram_bot.handler as handler

def registrar_comandos(app):
    # Comando /start
    app.add_handler(CommandHandler("start", handler.start_handler))
    
    
    # Comando /alertas
    alerta_handler = ConversationHandler(
        entry_points=[CommandHandler("alertas", handler.alerta_handler)],
        states={
            handler.UBI:[
                MessageHandler(filters.LOCATION, handler.ubicacion_alerta)
                #CommandHandler("skip", skip_location),
            ],
        },
        fallbacks=[CommandHandler("cancelar", handler.cancelar)],
    )
    app.add_handler(alerta_handler)

    # Respuesta a botones del menu
    app.add_handler(CallbackQueryHandler(handler.callback_handler))

    # ConversationHandler para el flujo de reportes
    reporte_handler = ConversationHandler(
        entry_points=[CommandHandler("reporte", handler.iniciar_reporte)],
        states={
            handler.UBICACION:[
                MessageHandler(filters.LOCATION, handler.recibir_ubicacion)
                #CommandHandler("skip", skip_location),
            ],
            handler.GRAVEDAD: [MessageHandler(filters.Regex("^(Muy Bajo|Bajo|Medio|Alto|Muy Alto)$"), handler.recibir_gravedad)],
            handler.PHOTO: [MessageHandler(filters.PHOTO, handler.recibir_comentario), CommandHandler("saltar", handler.skip_photo)],
            handler.COMENTARIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, handler.recibir_comentario)],
        },
        fallbacks=[CommandHandler("cancelar", handler.cancelar)],
    )

    app.add_handler(reporte_handler)

    # Respuesta a texto

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handler.mensaje_libre_handler))
     # Captura ubicación

    app.add_handler(MessageHandler(filters.LOCATION, handler.handle_location)) 
