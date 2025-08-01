import os
from dotenv import load_dotenv

load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# API Keys
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY', '')
BINANCE_API_KEY = os.getenv('BINANCE_API_KEY', '')
BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY', '')

# Telegram Channel
TELEGRAM_CHANNEL = "https://t.me/cryptovektorpro"

# Languages
LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇺🇸 English', 
    'de': '🇩🇪 Deutsch'
}

# Popular cryptocurrencies for notifications
POPULAR_COINS = [
    'bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana',
    'xrp', 'polkadot', 'dogecoin', 'avalanche-2', 'polygon',
    'shiba-inu', 'chainlink', 'litecoin', 'uniswap', 'cosmos'
]

# Time intervals for notifications
TIME_INTERVALS = {
    '15m': 15,
    '30m': 30, 
    '1h': 60,
    '3h': 180,
    '6h': 360,
    '12h': 720,
    '24h': 1440
}

# Multilingual text
TEXTS = {
    'ru': {
        'welcome': f"""
🚀 <b>Добро пожаловать в CryptoVektorProBot!</b> 🚀

Этот бот поможет вам отслеживать криптовалютный рынок в режиме реального времени.

📊 <b>Возможности бота:</b>
• Глобальная метрика рынка
• Топ-10 монет
• Топ пар Binance
• Индекс страха/жадности
• Тренды рынка
• DeFi метрики
• Настройка уведомлений

📢 <b>Наш канал:</b> {TELEGRAM_CHANNEL}

Выберите действие в меню ниже 👇
        """,
        'choose_language': 'Выберите язык:',
        'language_set': 'Язык установлен на русский 🇷🇺',
        'main_menu': 'Главное меню',
        'global_metrics': '🌍 Глобальная метрика',
        'top_10_coins': '🏆 Топ-10 монет',
        'binance_pairs': '💱 Топ пары Binance',
        'fear_greed': '😰 Индекс страха/жадности',
        'trends': '📈 Тренды',
        'defi_metrics': '🔗 DeFi метрики',
        'notifications': '🔔 Уведомления',
        'update_info': '🔄 Обновить информацию',
        'channel_link': '📢 Наш канал',
        'back': '⬅️ Назад',
        'choose_coin': 'Выберите монету:',
        'choose_interval': 'Выберите интервал уведомлений:',
        'notification_set': 'Уведомления настроены для {coin} каждые {interval}',
        'loading': 'Загрузка данных...',
        'error': 'Произошла ошибка при получении данных',
        'no_data': 'Данные недоступны'
    },
    'en': {
        'welcome': f"""
🚀 <b>Welcome to CryptoVektorProBot!</b> 🚀

This bot will help you track the cryptocurrency market in real time.

📊 <b>Bot features:</b>
• Global market metrics
• Top 10 coins
• Top Binance pairs
• Fear & Greed Index
• Market trends
• DeFi metrics
• Notification setup

📢 <b>Our channel:</b> {TELEGRAM_CHANNEL}

Choose an action from the menu below 👇
        """,
        'choose_language': 'Choose language:',
        'language_set': 'Language set to English 🇺🇸',
        'main_menu': 'Main Menu',
        'global_metrics': '🌍 Global Metrics',
        'top_10_coins': '🏆 Top 10 Coins',
        'binance_pairs': '💱 Top Binance Pairs',
        'fear_greed': '😰 Fear & Greed Index',
        'trends': '📈 Trends',
        'defi_metrics': '🔗 DeFi Metrics',
        'notifications': '🔔 Notifications',
        'update_info': '🔄 Update Info',
        'channel_link': '📢 Our Channel',
        'back': '⬅️ Back',
        'choose_coin': 'Choose coin:',
        'choose_interval': 'Choose notification interval:',
        'notification_set': 'Notifications set for {coin} every {interval}',
        'loading': 'Loading data...',
        'error': 'Error occurred while fetching data',
        'no_data': 'Data unavailable'
    },
    'de': {
        'welcome': f"""
🚀 <b>Willkommen bei CryptoVektorProBot!</b> 🚀

Dieser Bot hilft Ihnen, den Kryptowährungsmarkt in Echtzeit zu verfolgen.

📊 <b>Bot-Funktionen:</b>
• Globale Marktmetriken
• Top 10 Münzen
• Top Binance-Paare
• Fear & Greed Index
• Markttrends
• DeFi-Metriken
• Benachrichtigungseinstellungen

📢 <b>Unser Kanal:</b> {TELEGRAM_CHANNEL}

Wählen Sie eine Aktion aus dem Menü unten 👇
        """,
        'choose_language': 'Sprache wählen:',
        'language_set': 'Sprache auf Deutsch eingestellt 🇩🇪',
        'main_menu': 'Hauptmenü',
        'global_metrics': '🌍 Globale Metriken',
        'top_10_coins': '🏆 Top 10 Münzen',
        'binance_pairs': '💱 Top Binance-Paare',
        'fear_greed': '😰 Fear & Greed Index',
        'trends': '📈 Trends',
        'defi_metrics': '🔗 DeFi-Metriken',
        'notifications': '🔔 Benachrichtigungen',
        'update_info': '🔄 Info aktualisieren',
        'channel_link': '📢 Unser Kanal',
        'back': '⬅️ Zurück',
        'choose_coin': 'Münze wählen:',
        'choose_interval': 'Benachrichtigungsintervall wählen:',
        'notification_set': 'Benachrichtigungen für {coin} alle {interval} eingestellt',
        'loading': 'Daten werden geladen...',
        'error': 'Fehler beim Abrufen der Daten',
        'no_data': 'Daten nicht verfügbar'
    }
}