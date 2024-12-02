# bot.py

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers.handlers import Handlers
from config.config import TELEGRAM_BOT_TOKEN


class Bot:
    def __init__(self):
        self.application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
        self.handlers = Handlers()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler("start", self.handlers.start))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("menu", self.handlers.start))  
        self.application.add_handler(CallbackQueryHandler(self.handlers.button_handler))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message))

    def run(self):
        self.application.run_polling()
