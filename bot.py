import os

import telebot
from dotenv import load_dotenv

from weather import build_forecast_markdown

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise SystemExit("BOT_TOKEN не задан в файле .env")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_weather(message):
    bot.send_chat_action(message.chat.id, "typing")
    try:
        forecast = build_forecast_markdown()
    except Exception as error:
        print(f"Ошибка получения прогноза: {error}")
        bot.reply_to(message, "Не удалось получить прогноз. Попробуйте позже.")
        return

    bot.send_message(
        message.chat.id,
        forecast,
        parse_mode="MarkdownV2",
        disable_web_page_preview=True,
    )


if __name__ == "__main__":
    print("Бот запущен")
    bot.infinity_polling()
