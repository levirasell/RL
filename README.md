# CryptoVektorProBot 🚀

Telegram бот для отслеживания криптовалютного рынка в режиме реального времени.

## 🌟 Возможности

- **Многоязычность**: Русский, Английский, Немецкий
- **Глобальная метрика рынка**: Общая капитализация, объем торгов, доминация
- **Топ-10 криптовалют**: Актуальные цены и изменения
- **Топ пары Binance**: Самые активные торговые пары
- **Индекс страха/жадности**: Настроения рынка
- **Трендовые монеты**: Популярные криптовалюты
- **DeFi метрики**: Данные о децентрализованных финансах
- **Уведомления**: Настраиваемые уведомления о изменениях цен
- **Интуитивный интерфейс**: Все функции через кнопки

## 📋 Требования

- Python 3.8+
- Telegram Bot Token (получить у @BotFather)

## 🛠 Установка

### 1. Клонирование и установка зависимостей

```bash
# Установите зависимости
pip install -r requirements.txt
```

### 2. Настройка

1. Создайте бота в Telegram:
   - Напишите @BotFather в Telegram
   - Выполните команду `/newbot`
   - Следуйте инструкциям и сохраните токен

2. Настройте файл `.env`:
   ```bash
   BOT_TOKEN=ВАШ_ТОКЕН_БОТА
   DEBUG=True
   ```

### 3. Запуск

```bash
python main.py
```

## 🎮 Использование

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Выберите язык интерфейса
4. Используйте кнопки для навигации по функциям

### Доступные функции:

- 🌍 **Глобальная метрика** - общая информация о рынке
- 🏆 **Топ-10 монет** - самые капитализированные криптовалюты
- 💱 **Топ пары Binance** - активные торговые пары
- 😰 **Индекс страха/жадности** - настроения рынка
- 📈 **Тренды** - популярные монеты
- 🔗 **DeFi метрики** - данные DeFi сектора
- 🔔 **Уведомления** - настройка персональных уведомлений
- 🔄 **Обновление** - актуализация данных

## 🔔 Настройка уведомлений

1. Выберите "🔔 Уведомления"
2. Выберите криптовалюту из списка
3. Установите интервал уведомлений:
   - 15 минут
   - 30 минут
   - 1 час
   - 3 часа
   - 6 часов
   - 12 часов
   - 24 часа

## 🌐 Деплой на хостинг

### Heroku

1. Создайте аккаунт на [Heroku](https://heroku.com)
2. Установите [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
3. Создайте файл `Procfile`:
   ```
   worker: python main.py
   ```
4. Деплой:
   ```bash
   heroku create your-bot-name
   heroku config:set BOT_TOKEN=ваш_токен
   git add .
   git commit -m "Initial commit"
   git push heroku main
   heroku ps:scale worker=1
   ```

### Railway

1. Зарегистрируйтесь на [Railway](https://railway.app)
2. Подключите GitHub репозиторий
3. Добавьте переменную окружения `BOT_TOKEN`
4. Деплой произойдет автоматически

### PythonAnywhere

1. Загрузите файлы на [PythonAnywhere](https://pythonanywhere.com)
2. Создайте виртуальное окружение
3. Установите зависимости
4. Настройте задачу (Task) для запуска бота

## 📊 API источники

- **CoinGecko API** - основные данные о криптовалютах
- **Binance API** - данные о торговых парах
- **Alternative.me** - индекс страха и жадности

## 🔧 Структура проекта

```
CryptoVektorProBot/
├── main.py              # Основной файл бота
├── config.py            # Конфигурация и настройки
├── crypto_api.py        # API для получения данных
├── keyboards.py         # Клавиатуры и кнопки
├── notifications.py     # Система уведомлений
├── requirements.txt     # Зависимости
├── .env                 # Переменные окружения
└── README.md           # Документация
```

## 🚀 Канал проекта

Подписывайтесь на наш Telegram канал: [@cryptovektorpro](https://t.me/cryptovektorpro)

## 📝 Лицензия

MIT License

## 🤝 Поддержка

Если у вас есть вопросы или предложения, свяжитесь с нами через Telegram канал.

---

**Создано с ❤️ для криптосообщества**