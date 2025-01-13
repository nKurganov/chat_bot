import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import cohere

# Загрузка токенов из .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Проверка токенов
if not TELEGRAM_BOT_TOKEN or not COHERE_API_KEY:
    print("Ошибка: Проверьте наличие TELEGRAM_BOT_TOKEN и COHERE_API_KEY в файле .env.")
    exit(1)

# Инициализация Cohere Client V2
co = cohere.Client(api_key=COHERE_API_KEY)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я чат-бот, созданный студентом группы РИС-20-1бз Кургановым Н.В. "
        "Напишите что-нибудь, и я постараюсь ответить."
    )

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Используем метод chat для генерации ответа
        response = co.chat(
            model="command-r-plus-08-2024",  # Или другая доступная модель
            message=user_message
        )

        # Извлечение текста из ответа
        bot_reply = response.text.strip() if response.text else "Извините, я не смог ответить на ваш запрос."
        await update.message.reply_text(bot_reply)

    except cohere.CohereAPIError as e:
        # Обработка ошибок API Cohere
        await update.message.reply_text("Ошибка: Проблема с API Cohere. Проверьте запрос.")
        print(f"CohereError: {e}")

    except Exception as e:
        # Общая обработка ошибок
        await update.message.reply_text("Произошла ошибка при обработке запроса.")
        print(f"Error: {e}")

# Запуск бота
if __name__ == "__main__":
    try:
        app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    except Exception as e:
        print("Ошибка при инициализации Telegram бота. Проверьте TELEGRAM_BOT_TOKEN.")
        print(f"Error: {e}")
        exit(1)

    # Добавление обработчиков команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Ожидаем сообщения...")
    app.run_polling()