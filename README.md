# Weather Bot — Кабардино-Балкария

Минималистичный Telegram-бот на Python, который по команде `/start` присылает прогноз погоды на 7 дней для Нальчика (Кабардино-Балкарская Республика).

## Возможности

- Прогноз на 7 дней: температура, осадки, ветер, описание погоды
- Оформление в `MarkdownV2`: жирный шрифт, курсив, моноширинные значения, ссылка на источник
- Без эмодзи — только текст
- Данные из [Open-Meteo](https://open-meteo.com) — API без ключа и регистрации
- Токен хранится в `.env` и не попадает в репозиторий

## Стек

- Python 3.10+
- [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
- requests
- python-dotenv

## Структура проекта

```text
.
├── bot.py              # точка входа, обработчик /start
├── weather.py          # запрос к Open-Meteo и рендер MarkdownV2
├── requirements.txt    # зависимости
├── .env.example        # шаблон переменных окружения
├── .gitignore
└── README.md
```

## Установка

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Настройка

1. Получите токен у [@BotFather](https://t.me/BotFather).
2. Создайте `.env` на основе шаблона:

```bash
cp .env.example .env
```

3. Укажите токен:

```env
BOT_TOKEN=123456789:AA...
```

## Запуск

```bash
python bot.py
```

Откройте бота в Telegram и отправьте `/start`.

## Как это работает

`bot.py` принимает команду `/start`, вызывает `build_forecast_markdown()` из `weather.py`. Тот запрашивает дневной прогноз в Open-Meteo по координатам Нальчика (`43.4981, 43.6189`, часовой пояс `Europe/Moscow`) и собирает сообщение с экранированием всех динамических значений под `MarkdownV2`.

## Лицензия

Проект распространяется без лицензии. Добавьте `LICENSE`, если планируете открытое использование.
