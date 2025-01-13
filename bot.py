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
    await update.message.reply_text("Привет! Я чат-бот, созданный студентом группы РИС-20-1бз Кургановым Н.В. Напишите что-нибудь, и я постараюсь ответить.")

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Генерация ответа с использованием Cohere.ai
        response = co.generate(
            model='command-xlarge-nightly',  # Убедитесь, что модель поддерживает `generate`
            prompt=f"User: {user_message}\nBot:",
            max_tokens=150,
            temperature=0.7
        )
        bot_reply = response.generations[0].text.strip()
        await update.message.reply_text(bot_reply)

    except cohere.CohereError as e:
        # Обработка ошибок Cohere
        await update.message.reply_text("Ошибка на стороне Cohere. Проверьте настройки модели.")
        print(f"CohereError: {e}")

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
