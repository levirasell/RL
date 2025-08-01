import asyncio
import logging
from datetime import datetime
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

# Импорты наших модулей
from config import BOT_TOKEN, TEXTS, TELEGRAM_CHANNEL
from crypto_api import crypto_api
from keyboards import keyboards
from notifications import init_notification_manager

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class CryptoVektorProBot:
    def __init__(self):
        self.app = None
        self.notification_manager = None
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = str(update.effective_user.id)
        
        # Если пользователь уже выбрал язык, показываем главное меню
        if self.notification_manager and user_id in self.notification_manager.user_languages:
            language = self.notification_manager.get_user_language(user_id)
            texts = TEXTS[language]
            await update.message.reply_text(
                texts['welcome'],
                reply_markup=keyboards.get_main_menu_keyboard(language),
                parse_mode=ParseMode.HTML
            )
        else:
            # Предлагаем выбрать язык
            await update.message.reply_text(
                "🌍 Please choose your language / Bitte wählen Sie Ihre Sprache / Пожалуйста, выберите язык:",
                reply_markup=keyboards.get_language_keyboard()
            )
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        user_id = str(query.from_user.id)
        data = query.data
        
        # Получаем язык пользователя
        language = 'ru'
        if self.notification_manager:
            language = self.notification_manager.get_user_language(user_id)
        texts = TEXTS[language]
        
        try:
            # Обработка выбора языка
            if data.startswith('lang_'):
                lang_code = data.split('_')[1]
                if self.notification_manager:
                    self.notification_manager.set_user_language(user_id, lang_code)
                language = lang_code
                texts = TEXTS[language]
                
                await query.edit_message_text(
                    texts['welcome'],
                    reply_markup=keyboards.get_main_menu_keyboard(language),
                    parse_mode=ParseMode.HTML
                )
            
            # Возврат в главное меню
            elif data == 'back_to_menu':
                await query.edit_message_text(
                    texts['welcome'],
                    reply_markup=keyboards.get_main_menu_keyboard(language),
                    parse_mode=ParseMode.HTML
                )
            
            # Глобальная метрика
            elif data == 'global_metrics':
                await query.edit_message_text(
                    texts['loading'],
                    reply_markup=keyboards.get_back_keyboard(language)
                )
                
                global_data = await crypto_api.get_global_metrics()
                if global_data:
                    message = self.format_global_metrics(global_data, language)
                    await query.edit_message_text(
                        message,
                        reply_markup=keyboards.get_update_keyboard(language),
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await query.edit_message_text(
                        texts['error'],
                        reply_markup=keyboards.get_back_keyboard(language)
                    )
            
            # Топ-10 монет
            elif data == 'top_10_coins':
                await query.edit_message_text(
                    texts['loading'],
                    reply_markup=keyboards.get_back_keyboard(language)
                )
                
                top_coins = await crypto_api.get_top_coins()
                if top_coins:
                    message = self.format_top_coins(top_coins, language)
                    await query.edit_message_text(
                        message,
                        reply_markup=keyboards.get_update_keyboard(language),
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await query.edit_message_text(
                        texts['error'],
                        reply_markup=keyboards.get_back_keyboard(language)
                    )
            
            # Топ пары Binance
            elif data == 'binance_pairs':
                await query.edit_message_text(
                    texts['loading'],
                    reply_markup=keyboards.get_back_keyboard(language)
                )
                
                binance_pairs = await crypto_api.get_binance_top_pairs()
                if binance_pairs:
                    message = self.format_binance_pairs(binance_pairs, language)
                    await query.edit_message_text(
                        message,
                        reply_markup=keyboards.get_update_keyboard(language),
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await query.edit_message_text(
                        texts['error'],
                        reply_markup=keyboards.get_back_keyboard(language)
                    )
            
            # Индекс страха/жадности
            elif data == 'fear_greed':
                await query.edit_message_text(
                    texts['loading'],
                    reply_markup=keyboards.get_back_keyboard(language)
                )
                
                fear_greed = await crypto_api.get_fear_greed_index()
                if fear_greed:
                    message = self.format_fear_greed(fear_greed, language)
                    await query.edit_message_text(
                        message,
                        reply_markup=keyboards.get_update_keyboard(language),
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await query.edit_message_text(
                        texts['error'],
                        reply_markup=keyboards.get_back_keyboard(language)
                    )
            
            # Тренды
            elif data == 'trends':
                await query.edit_message_text(
                    texts['loading'],
                    reply_markup=keyboards.get_back_keyboard(language)
                )
                
                trends = await crypto_api.get_trending_coins()
                if trends:
                    message = self.format_trends(trends, language)
                    await query.edit_message_text(
                        message,
                        reply_markup=keyboards.get_update_keyboard(language),
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await query.edit_message_text(
                        texts['error'],
                        reply_markup=keyboards.get_back_keyboard(language)
                    )
            
            # DeFi метрики
            elif data == 'defi_metrics':
                await query.edit_message_text(
                    texts['loading'],
                    reply_markup=keyboards.get_back_keyboard(language)
                )
                
                defi_data = await crypto_api.get_defi_metrics()
                if defi_data:
                    message = self.format_defi_metrics(defi_data, language)
                    await query.edit_message_text(
                        message,
                        reply_markup=keyboards.get_update_keyboard(language),
                        parse_mode=ParseMode.HTML
                    )
                else:
                    await query.edit_message_text(
                        texts['error'],
                        reply_markup=keyboards.get_back_keyboard(language)
                    )
            
            # Уведомления
            elif data == 'notifications':
                await query.edit_message_text(
                    texts['choose_coin'],
                    reply_markup=keyboards.get_coins_keyboard(language)
                )
            
            # Выбор монеты для уведомлений
            elif data.startswith('coin_'):
                coin_id = data.split('_', 1)[1]
                await query.edit_message_text(
                    texts['choose_interval'],
                    reply_markup=keyboards.get_intervals_keyboard(coin_id, language)
                )
            
            # Выбор интервала уведомлений
            elif data.startswith('interval_'):
                parts = data.split('_')
                coin_id = parts[1]
                interval = parts[2]
                
                if self.notification_manager:
                    self.notification_manager.add_notification(user_id, coin_id, interval)
                    
                    # Получаем информацию о монете для отображения
                    coin_data = await crypto_api.get_coin_info(coin_id)
                    coin_name = coin_data['name'] if coin_data else coin_id
                    
                    interval_text = interval
                    if language == 'ru':
                        interval_names = {'15m': '15 минут', '30m': '30 минут', '1h': '1 час', 
                                        '3h': '3 часа', '6h': '6 часов', '12h': '12 часов', '24h': '24 часа'}
                        interval_text = interval_names.get(interval, interval)
                    elif language == 'en':
                        interval_names = {'15m': '15 minutes', '30m': '30 minutes', '1h': '1 hour', 
                                        '3h': '3 hours', '6h': '6 hours', '12h': '12 hours', '24h': '24 hours'}
                        interval_text = interval_names.get(interval, interval)
                    elif language == 'de':
                        interval_names = {'15m': '15 Minuten', '30m': '30 Minuten', '1h': '1 Stunde', 
                                        '3h': '3 Stunden', '6h': '6 Stunden', '12h': '12 Stunden', '24h': '24 Stunden'}
                        interval_text = interval_names.get(interval, interval)
                    
                    message = texts['notification_set'].format(coin=coin_name, interval=interval_text)
                    await query.edit_message_text(
                        message,
                        reply_markup=keyboards.get_back_keyboard(language)
                    )
            
            # Обновление информации
            elif data == 'update_info' or data == 'update_current':
                # Возвращаем пользователя в главное меню
                await query.edit_message_text(
                    texts['welcome'],
                    reply_markup=keyboards.get_main_menu_keyboard(language),
                    parse_mode=ParseMode.HTML
                )
                
        except Exception as e:
            logger.error(f"Error in button handler: {e}")
            await query.edit_message_text(
                texts['error'],
                reply_markup=keyboards.get_back_keyboard(language)
            )
    
    def format_global_metrics(self, data, language):
        """Форматирует глобальную метрику"""
        change_emoji = "🟢" if data['market_cap_change_24h'] > 0 else "🔴"
        change_sign = "+" if data['market_cap_change_24h'] > 0 else ""
        
        if language == 'ru':
            return f"""
🌍 <b>Глобальная метрика крипторынка</b>

💰 <b>Общая капитализация:</b> ${data['total_market_cap_usd']:,.0f}
💹 <b>Общий объем 24ч:</b> ${data['total_volume_24h_usd']:,.0f}
{change_emoji} <b>Изменение капитализации 24ч:</b> {change_sign}{data['market_cap_change_24h']:.2f}%

🪙 <b>Активные криптовалюты:</b> {data['active_cryptocurrencies']:,}
🏪 <b>Биржи:</b> {data['markets']:,}

📊 <b>Доминация:</b>
• Bitcoin: {data['market_cap_percentage'].get('btc', 0):.1f}%
• Ethereum: {data['market_cap_percentage'].get('eth', 0):.1f}%

⏰ <i>Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        elif language == 'en':
            return f"""
🌍 <b>Global Crypto Market Metrics</b>

💰 <b>Total Market Cap:</b> ${data['total_market_cap_usd']:,.0f}
💹 <b>Total 24h Volume:</b> ${data['total_volume_24h_usd']:,.0f}
{change_emoji} <b>Market Cap Change 24h:</b> {change_sign}{data['market_cap_change_24h']:.2f}%

🪙 <b>Active Cryptocurrencies:</b> {data['active_cryptocurrencies']:,}
🏪 <b>Markets:</b> {data['markets']:,}

📊 <b>Dominance:</b>
• Bitcoin: {data['market_cap_percentage'].get('btc', 0):.1f}%
• Ethereum: {data['market_cap_percentage'].get('eth', 0):.1f}%

⏰ <i>Updated: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        else:  # German
            return f"""
🌍 <b>Globale Krypto-Marktmetriken</b>

💰 <b>Gesamte Marktkapitalisierung:</b> ${data['total_market_cap_usd']:,.0f}
💹 <b>Gesamtes 24h Volumen:</b> ${data['total_volume_24h_usd']:,.0f}
{change_emoji} <b>Marktkapitalisierung Änderung 24h:</b> {change_sign}{data['market_cap_change_24h']:.2f}%

🪙 <b>Aktive Kryptowährungen:</b> {data['active_cryptocurrencies']:,}
🏪 <b>Märkte:</b> {data['markets']:,}

📊 <b>Dominanz:</b>
• Bitcoin: {data['market_cap_percentage'].get('btc', 0):.1f}%
• Ethereum: {data['market_cap_percentage'].get('eth', 0):.1f}%

⏰ <i>Aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
    
    def format_top_coins(self, coins, language):
        """Форматирует топ монет"""
        if language == 'ru':
            message = "🏆 <b>Топ-10 криптовалют</b>\n\n"
        elif language == 'en':
            message = "🏆 <b>Top 10 Cryptocurrencies</b>\n\n"
        else:
            message = "🏆 <b>Top 10 Kryptowährungen</b>\n\n"
        
        for coin in coins:
            emoji = "🟢" if coin['price_change_24h'] > 0 else "🔴"
            sign = "+" if coin['price_change_24h'] > 0 else ""
            
            message += f"""
<b>{coin['rank']}. {coin['name']} ({coin['symbol']})</b>
💰 ${coin['price']:,.2f} {emoji} {sign}{coin['price_change_24h']:.2f}%
📈 Cap: ${coin['market_cap']:,.0f}

"""
        
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        if language == 'ru':
            message += f"⏰ <i>Обновлено: {timestamp}</i>"
        elif language == 'en':
            message += f"⏰ <i>Updated: {timestamp}</i>"
        else:
            message += f"⏰ <i>Aktualisiert: {timestamp}</i>"
        
        return message
    
    def format_binance_pairs(self, pairs, language):
        """Форматирует топ пары Binance"""
        if language == 'ru':
            message = "💱 <b>Топ пары Binance (USDT)</b>\n\n"
        elif language == 'en':
            message = "💱 <b>Top Binance Pairs (USDT)</b>\n\n"
        else:
            message = "💱 <b>Top Binance-Paare (USDT)</b>\n\n"
        
        for i, pair in enumerate(pairs, 1):
            emoji = "🟢" if pair['price_change_24h'] > 0 else "🔴"
            sign = "+" if pair['price_change_24h'] > 0 else ""
            
            message += f"""
<b>{i}. {pair['symbol']}</b>
💰 ${pair['price']:,.4f} {emoji} {sign}{pair['price_change_24h']:.2f}%
💹 24h Vol: ${pair['volume_24h']:,.0f}

"""
        
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        if language == 'ru':
            message += f"⏰ <i>Обновлено: {timestamp}</i>"
        elif language == 'en':
            message += f"⏰ <i>Updated: {timestamp}</i>"
        else:
            message += f"⏰ <i>Aktualisiert: {timestamp}</i>"
        
        return message
    
    def format_fear_greed(self, data, language):
        """Форматирует индекс страха/жадности"""
        if language == 'ru':
            message = f"""
😰 <b>Индекс страха и жадности</b>

{data['emoji']} <b>Значение:</b> {data['value']}/100
📊 <b>Статус:</b> {data['status']}

⏰ <i>Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        elif language == 'en':
            message = f"""
😰 <b>Fear & Greed Index</b>

{data['emoji']} <b>Value:</b> {data['value']}/100
📊 <b>Status:</b> {data['status']}

⏰ <i>Updated: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        else:  # German
            message = f"""
😰 <b>Fear & Greed Index</b>

{data['emoji']} <b>Wert:</b> {data['value']}/100
📊 <b>Status:</b> {data['status']}

⏰ <i>Aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        
        return message
    
    def format_trends(self, trends, language):
        """Форматирует трендовые монеты"""
        if language == 'ru':
            message = "📈 <b>Трендовые монеты</b>\n\n"
        elif language == 'en':
            message = "📈 <b>Trending Coins</b>\n\n"
        else:
            message = "📈 <b>Trend-Münzen</b>\n\n"
        
        for i, coin in enumerate(trends, 1):
            rank_text = f"#{coin['market_cap_rank']}" if coin['market_cap_rank'] else "N/A"
            message += f"<b>{i}. {coin['name']} ({coin['symbol']})</b> - Rank: {rank_text}\n"
        
        timestamp = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        if language == 'ru':
            message += f"\n⏰ <i>Обновлено: {timestamp}</i>"
        elif language == 'en':
            message += f"\n⏰ <i>Updated: {timestamp}</i>"
        else:
            message += f"\n⏰ <i>Aktualisiert: {timestamp}</i>"
        
        return message
    
    def format_defi_metrics(self, data, language):
        """Форматирует DeFi метрики"""
        if language == 'ru':
            message = f"""
🔗 <b>DeFi Метрики</b>

💰 <b>DeFi Капитализация:</b> ${data['defi_market_cap']:,.0f}
⚡ <b>ETH Капитализация:</b> ${data['eth_market_cap']:,.0f}
📊 <b>DeFi/ETH Отношение:</b> {data['defi_to_eth_ratio']:.2f}%
💹 <b>Объем торгов 24ч:</b> ${data['trading_volume_24h']:,.0f}
🏆 <b>DeFi Доминация:</b> {data['defi_dominance']:.2f}%

⏰ <i>Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        elif language == 'en':
            message = f"""
🔗 <b>DeFi Metrics</b>

💰 <b>DeFi Market Cap:</b> ${data['defi_market_cap']:,.0f}
⚡ <b>ETH Market Cap:</b> ${data['eth_market_cap']:,.0f}
📊 <b>DeFi/ETH Ratio:</b> {data['defi_to_eth_ratio']:.2f}%
💹 <b>24h Trading Volume:</b> ${data['trading_volume_24h']:,.0f}
🏆 <b>DeFi Dominance:</b> {data['defi_dominance']:.2f}%

⏰ <i>Updated: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        else:  # German
            message = f"""
🔗 <b>DeFi-Metriken</b>

💰 <b>DeFi-Marktkapitalisierung:</b> ${data['defi_market_cap']:,.0f}
⚡ <b>ETH-Marktkapitalisierung:</b> ${data['eth_market_cap']:,.0f}
📊 <b>DeFi/ETH-Verhältnis:</b> {data['defi_to_eth_ratio']:.2f}%
💹 <b>24h Handelsvolumen:</b> ${data['trading_volume_24h']:,.0f}
🏆 <b>DeFi-Dominanz:</b> {data['defi_dominance']:.2f}%

⏰ <i>Aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        
        return message
    
    async def run(self):
        """Запуск бота"""
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment variables!")
            return
        
        # Создаем приложение
        self.app = Application.builder().token(BOT_TOKEN).build()
        
        # Инициализируем менеджер уведомлений
        self.notification_manager = init_notification_manager(self.app.bot)
        
        # Добавляем обработчики
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
        
        # Запускаем планировщик уведомлений
        self.notification_manager.start_scheduler()
        
        logger.info("Bot started successfully!")
        
        try:
            # Запускаем бота
            await self.app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e:
            logger.error(f"Error during polling: {e}")
        finally:
            # Останавливаем планировщик при завершении
            if self.notification_manager:
                self.notification_manager.stop_scheduler()
            logger.info("Bot stopped")

async def main():
    """Главная функция"""
    bot = CryptoVektorProBot()
    await bot.run()

def start_bot():
    """Запуск бота с обработкой event loop"""
    try:
        # Попробуем использовать asyncio.run()
        asyncio.run(main())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            # Если event loop уже запущен, создаем новый
            logger.info("Creating new event loop...")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(main())
            finally:
                loop.close()
        else:
            raise e
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        # Последняя попытка с новым event loop
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(main())
            loop.close()
        except Exception as final_error:
            logger.error(f"Final error: {final_error}")
            raise

if __name__ == '__main__':
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")