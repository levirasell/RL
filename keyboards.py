from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from config import LANGUAGES, POPULAR_COINS, TIME_INTERVALS, TELEGRAM_CHANNEL, TEXTS

class BotKeyboards:
    @staticmethod
    def get_language_keyboard():
        """Клавиатура выбора языка"""
        keyboard = []
        for lang_code, lang_name in LANGUAGES.items():
            keyboard.append([InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}")])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_main_menu_keyboard(lang='ru'):
        """Главное меню"""
        texts = TEXTS[lang]
        keyboard = [
            [InlineKeyboardButton(texts['global_metrics'], callback_data='global_metrics')],
            [InlineKeyboardButton(texts['top_10_coins'], callback_data='top_10_coins')],
            [InlineKeyboardButton(texts['binance_pairs'], callback_data='binance_pairs')],
            [InlineKeyboardButton(texts['fear_greed'], callback_data='fear_greed')],
            [InlineKeyboardButton(texts['trends'], callback_data='trends')],
            [InlineKeyboardButton(texts['defi_metrics'], callback_data='defi_metrics')],
            [InlineKeyboardButton(texts['notifications'], callback_data='notifications')],
            [InlineKeyboardButton(texts['update_info'], callback_data='update_info')],
            [InlineKeyboardButton(texts['channel_link'], url=TELEGRAM_CHANNEL)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_back_keyboard(lang='ru'):
        """Кнопка "Назад" """
        texts = TEXTS[lang]
        keyboard = [[InlineKeyboardButton(texts['back'], callback_data='back_to_menu')]]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_coins_keyboard(lang='ru'):
        """Клавиатура выбора монет для уведомлений"""
        texts = TEXTS[lang]
        keyboard = []
        
        # Названия монет для отображения
        coin_names = {
            'bitcoin': 'Bitcoin (BTC)',
            'ethereum': 'Ethereum (ETH)',
            'binancecoin': 'Binance Coin (BNB)',
            'cardano': 'Cardano (ADA)',
            'solana': 'Solana (SOL)',
            'xrp': 'XRP (XRP)',
            'polkadot': 'Polkadot (DOT)',
            'dogecoin': 'Dogecoin (DOGE)',
            'avalanche-2': 'Avalanche (AVAX)',
            'polygon': 'Polygon (MATIC)',
            'shiba-inu': 'Shiba Inu (SHIB)',
            'chainlink': 'Chainlink (LINK)',
            'litecoin': 'Litecoin (LTC)',
            'uniswap': 'Uniswap (UNI)',
            'cosmos': 'Cosmos (ATOM)'
        }
        
        # Создаем кнопки по 2 в ряд
        for i in range(0, len(POPULAR_COINS), 2):
            row = []
            for j in range(2):
                if i + j < len(POPULAR_COINS):
                    coin_id = POPULAR_COINS[i + j]
                    coin_name = coin_names.get(coin_id, coin_id.capitalize())
                    row.append(InlineKeyboardButton(coin_name, callback_data=f"coin_{coin_id}"))
            keyboard.append(row)
        
        # Добавляем кнопку "Назад"
        keyboard.append([InlineKeyboardButton(texts['back'], callback_data='back_to_menu')])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def get_intervals_keyboard(coin_id, lang='ru'):
        """Клавиатура выбора интервалов уведомлений"""
        texts = TEXTS[lang]
        keyboard = []
        
        # Названия интервалов
        interval_names = {
            '15m': '15 минут',
            '30m': '30 минут',
            '1h': '1 час',
            '3h': '3 часа',
            '6h': '6 часов',
            '12h': '12 часов',
            '24h': '24 часа'
        }
        
        if lang == 'en':
            interval_names = {
                '15m': '15 minutes',
                '30m': '30 minutes',
                '1h': '1 hour',
                '3h': '3 hours',
                '6h': '6 hours',
                '12h': '12 hours',
                '24h': '24 hours'
            }
        elif lang == 'de':
            interval_names = {
                '15m': '15 Minuten',
                '30m': '30 Minuten',
                '1h': '1 Stunde',
                '3h': '3 Stunden',
                '6h': '6 Stunden',
                '12h': '12 Stunden',
                '24h': '24 Stunden'
            }
        
        # Создаем кнопки по 2 в ряд
        intervals = list(TIME_INTERVALS.keys())
        for i in range(0, len(intervals), 2):
            row = []
            for j in range(2):
                if i + j < len(intervals):
                    interval = intervals[i + j]
                    interval_name = interval_names[interval]
                    row.append(InlineKeyboardButton(interval_name, callback_data=f"interval_{coin_id}_{interval}"))
            keyboard.append(row)
        
        # Добавляем кнопки навигации
        keyboard.append([InlineKeyboardButton(texts['back'], callback_data='notifications')])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod 
    def get_update_keyboard(lang='ru'):
        """Клавиатура с кнопкой обновления"""
        texts = TEXTS[lang]
        keyboard = [
            [InlineKeyboardButton(texts['update_info'], callback_data='update_current')],
            [InlineKeyboardButton(texts['back'], callback_data='back_to_menu')]
        ]
        return InlineKeyboardMarkup(keyboard)

# Создаем глобальный экземпляр клавиатур
keyboards = BotKeyboards()