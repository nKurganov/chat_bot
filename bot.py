import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import cohere
from cohere.error import CohereError, BadRequestError

# Загрузка токенов из .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Инициализация Cohere Client
co = cohere.Client(api_key=COHERE_API_KEY)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я чат-бот, созданный студентом группы РИС-20-1бз Кургановым Н.В. Напишите что-нибудь, и я постараюсь ответить."
    )

# Обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Используем Chat API для генерации ответа
        response = co.chat(
            model="command-r-plus",  # Убедитесь, что модель поддерживает Chat API
            messages=[{"role": "user", "content": user_message}]
        )

        # Извлечение текста из ответа
        bot_reply = response.message.content if response.message else "Извините, я не смог ответить на ваш запрос."
        await update.message.reply_text(bot_reply)

    except BadRequestError as e:
        # Обработка ошибок неверного запроса
        await update.message.reply_text("Ошибка: Неверный запрос к API Cohere. Проверьте ваш запрос.")
        print(f"BadRequestError: {e}")

    except CohereError as e:
        # Обработка ошибок API Cohere
        await update.message.reply_text("Ошибка: Проблема с API Cohere.")
        print(f"CohereError: {e}")

    except Exception as e:
        # Общая обработка ошибок
        await update.message.reply_text("Произошла ошибка при обработке запроса.")
        print(f"Error: {e}")

# Запуск бота
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Добавление обработчиков команд и сообщений
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Ожидаем сообщения...")
    app.run_polling()
