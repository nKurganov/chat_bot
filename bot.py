import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import cohere

# Загрузка токенов из .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Настройка Cohere API
co = cohere.Client(COHERE_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я чат-бот, созданный студентом группы РИС-20-1бз Кургановым Н.В. Напишите что-нибудь, и я постараюсь ответить."
    )

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Используем Chat API для генерации ответа
        response = co.chat(
            query=user_message,
            model='command-r7b-12-2024-vllm',  # Подходящая модель
            chat_history=[],  # Если нужна история чата, добавьте предыдущие сообщения
            temperature=0.7
        )
        bot_reply = response.reply
        await update.message.reply_text(bot_reply)

    except cohere.errors.BadRequestError as e:
        # Обработка ошибок некорректного запроса
        await update.message.reply_text("Ошибка: Некорректный запрос к API Cohere.")
        print(f"BadRequestError: {e}")

    except Exception as e:
        # Общая обработка ошибок
        await update.message.reply_text("Произошла ошибка при обработке запроса.")
        print(f"Error: {e}")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Обработчики команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Ожидаем сообщения...")
    app.run_polling()
