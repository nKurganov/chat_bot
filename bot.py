import os
try:
    from telegram import Update
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
except ModuleNotFoundError:
    print("Ошибка: Модуль 'telegram' не найден. Убедитесь, что библиотека 'python-telegram-bot' установлена.")
    exit(1)

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
co = cohere.ClientV2(api_key=COHERE_API_KEY)

# Обработчик команды /start
def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    update.message.reply_text(
        "Привет! Я чат-бот, созданный студентом группы РИС-20-1бз Кургановым Н.В. "
        "Напишите что-нибудь, и я постараюсь ответить."
    )

# Обработчик сообщений
def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Используем метод chat для генерации ответа
        response = co.chat(
            model="command-r-plus-08-2024",  # Или другая доступная модель
            messages=[{"role": "user", "content": user_message}]
        )

        # Извлечение текста из ответа
        # По документации Cohere Chat API: response.text -> основной ответ
        bot_reply = response.text.strip() if response.text else "Извините, я не смог ответить на ваш запрос."
        update.message.reply_text(bot_reply)

    except cohere.CohereError as e:
        # Обработка ошибок API Cohere
        update.message.reply_text("Ошибка: Проблема с API Cohere. Проверьте запрос.")
        print(f"CohereError: {e}")

    except Exception as e:
        # Общая обработка ошибок
        update.message.reply_text("Произошла ошибка при обработке запроса.")
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


# -------------------------------------------------
# TEST CASES (pseudo-code / placeholders):
# -------------------------------------------------
# 1. Test basic greeting:
#    Input:  "Привет!"
#    Expect: Bot replies with a coherent greeting or some default response.
#
# 2. Test empty message:
#    Input:  ""
#    Expect: Bot might reply with "Извините, я не смог ответить на ваш запрос." 
#    (Please confirm if that's the desired behavior!)
#
# 3. Test longer text:
#    Input:  "Расскажи мне о космических исследованиях, пожалуйста."
#    Expect: Bot returns some short summary about space exploration.
#
# 4. Test special characters or unusual input:
#    Input:  "@#$%^&*()!"
#    Expect: Bot either responds with some default fallback or an error message.
#
# -------------------------------------------------
# PLEASE CLARIFY:
# -------------------------------------------------
# - What should happen if the user sends an empty message or unsupported characters?
# - Do you want fallback responses for certain categories of input?
#
# Feel free to describe your expected behavior in these scenarios, and we can adjust the code accordingly.
