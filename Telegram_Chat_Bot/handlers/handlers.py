# handlers.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from search.search import Search
from config.config import BROWSER_CHOICE


class Handlers:
    def __init__(self):
        self.search = Search(BROWSER_CHOICE)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.callback_query.message if update.callback_query else update.effective_message
        keyboard = [
            [InlineKeyboardButton("Старт", callback_data='start_search')],
            [InlineKeyboardButton("Помощь", callback_data='help')],
            [InlineKeyboardButton("Выбор браузера", callback_data='choose_browser')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text('Привет! Я бот, который может искать информацию в интернете. Выберите опцию:',
                                 reply_markup=reply_markup)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.callback_query.message if update.callback_query else update.effective_message
        help_text = (
            "Доступные команды:\n"
            "/start - Запустить бота\n"
            "/menu - Открыть главное меню\n"
            "/help - Получить помощь\n"
            "/set_browser <browser> - Установить браузер (chrome, firefox, edge)\n"
            "Просто напишите сообщение, и я постараюсь ответить на ваш вопрос!"
        )
        await message.reply_text(help_text)

    async def choose_browser(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.callback_query.message
        keyboard = [
            [InlineKeyboardButton("Chrome", callback_data='set_browser_chrome')],
            [InlineKeyboardButton("Firefox", callback_data='set_browser_firefox')],
            [InlineKeyboardButton("Edge", callback_data='set_browser_edge')],
            [InlineKeyboardButton("Назад", callback_data='back_to_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text('Выберите браузер:', reply_markup=reply_markup)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text
        if user_message.lower() == "стоп":
            await self.stop_searching(update, context)
            return

        await update.message.reply_text("Ищу информацию...")
        chat_id = update.message.chat_id
        await self.search.search_internet(user_message, chat_id, context)

    async def stop_searching(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Поиск остановлен.")

    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()  # Подтверждаем нажатие кнопки

        if query.data == 'start_search':
            await query.message.reply_text("Введите ваш запрос для поиска.")
        elif query.data == 'help':
            await self.help_command(update, context)
        elif query.data == 'choose_browser':
            await self.choose_browser(update, context)
        elif query.data.startswith('set_browser_'):
            browser_choice = query.data.split('_')[-1]
            # Здесь можно установить браузер, например, сохранить в конфигурации
            await query.message.reply_text(f"Браузер установлен на: {browser_choice.capitalize()}")
        elif query.data == 'back_to_menu':
            await self.start(update, context)
