import asyncio
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from crypto_api import crypto_api
from config import TIME_INTERVALS, TEXTS

class NotificationManager:
    def __init__(self, bot):
        self.bot = bot
        self.scheduler = AsyncIOScheduler()
        self.user_notifications = {}  # {user_id: {coin_id: interval}}
        self.user_languages = {}  # {user_id: language}
        self.data_file = 'user_data.json'
        self.load_user_data()
        
    def load_user_data(self):
        """Загружает данные пользователей из файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_notifications = data.get('notifications', {})
                    self.user_languages = data.get('languages', {})
        except Exception as e:
            print(f"Error loading user data: {e}")
    
    def save_user_data(self):
        """Сохраняет данные пользователей в файл"""
        try:
            data = {
                'notifications': self.user_notifications,
                'languages': self.user_languages
            }
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")
    
    def set_user_language(self, user_id: str, language: str):
        """Устанавливает язык пользователя"""
        self.user_languages[user_id] = language
        self.save_user_data()
    
    def get_user_language(self, user_id: str) -> str:
        """Получает язык пользователя"""
        return self.user_languages.get(user_id, 'ru')
    
    def add_notification(self, user_id: str, coin_id: str, interval: str):
        """Добавляет уведомление для пользователя"""
        if user_id not in self.user_notifications:
            self.user_notifications[user_id] = {}
        
        # Удаляем старое уведомление для этой монеты, если есть
        if coin_id in self.user_notifications[user_id]:
            self.remove_notification(user_id, coin_id)
        
        self.user_notifications[user_id][coin_id] = interval
        self.save_user_data()
        
        # Создаем задачу в планировщике
        job_id = f"{user_id}_{coin_id}"
        minutes = TIME_INTERVALS[interval]
        
        self.scheduler.add_job(
            func=self.send_coin_update,
            trigger='interval',
            minutes=minutes,
            args=[user_id, coin_id],
            id=job_id,
            replace_existing=True
        )
    
    def remove_notification(self, user_id: str, coin_id: str):
        """Удаляет уведомление"""
        if user_id in self.user_notifications and coin_id in self.user_notifications[user_id]:
            del self.user_notifications[user_id][coin_id]
            self.save_user_data()
            
            # Удаляем задачу из планировщика
            job_id = f"{user_id}_{coin_id}"
            try:
                self.scheduler.remove_job(job_id)
            except:
                pass
    
    def get_user_notifications(self, user_id: str) -> Dict:
        """Получает список уведомлений пользователя"""
        return self.user_notifications.get(user_id, {})
    
    async def send_coin_update(self, user_id: str, coin_id: str):
        """Отправляет обновление о монете"""
        try:
            language = self.get_user_language(user_id)
            texts = TEXTS[language]
            
            # Получаем данные о монете
            coin_data = await crypto_api.get_coin_info(coin_id)
            
            if coin_data:
                # Формируем сообщение
                message = self.format_coin_message(coin_data, language)
                
                # Отправляем сообщение
                await self.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='HTML'
                )
            else:
                await self.bot.send_message(
                    chat_id=user_id,
                    text=texts['error']
                )
                
        except Exception as e:
            print(f"Error sending notification to {user_id}: {e}")
    
    def format_coin_message(self, coin_data: Dict, language: str) -> str:
        """Форматирует сообщение о монете"""
        texts = TEXTS[language]
        
        # Эмодзи для изменения цены
        price_emoji = "🟢" if coin_data['price_change_24h'] > 0 else "🔴"
        price_change_sign = "+" if coin_data['price_change_24h'] > 0 else ""
        
        if language == 'ru':
            message = f"""
🪙 <b>{coin_data['name']} ({coin_data['symbol']})</b>

💰 <b>Цена:</b> ${coin_data['current_price']:,.2f}
{price_emoji} <b>Изменение 24ч:</b> {price_change_sign}{coin_data['price_change_24h']:.2f}%
📊 <b>Изменение 7д:</b> {coin_data['price_change_7d']:.2f}%
🏆 <b>Ранг:</b> #{coin_data['market_cap_rank']}
📈 <b>Рын. капитализация:</b> ${coin_data['market_cap']:,.0f}
💹 <b>Объем 24ч:</b> ${coin_data['volume_24h']:,.0f}

⏰ <i>Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        elif language == 'en':
            message = f"""
🪙 <b>{coin_data['name']} ({coin_data['symbol']})</b>

💰 <b>Price:</b> ${coin_data['current_price']:,.2f}
{price_emoji} <b>24h Change:</b> {price_change_sign}{coin_data['price_change_24h']:.2f}%
📊 <b>7d Change:</b> {coin_data['price_change_7d']:.2f}%
🏆 <b>Rank:</b> #{coin_data['market_cap_rank']}
📈 <b>Market Cap:</b> ${coin_data['market_cap']:,.0f}
💹 <b>24h Volume:</b> ${coin_data['volume_24h']:,.0f}

⏰ <i>Updated: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        else:  # German
            message = f"""
🪙 <b>{coin_data['name']} ({coin_data['symbol']})</b>

💰 <b>Preis:</b> ${coin_data['current_price']:,.2f}
{price_emoji} <b>24h Änderung:</b> {price_change_sign}{coin_data['price_change_24h']:.2f}%
📊 <b>7d Änderung:</b> {coin_data['price_change_7d']:.2f}%
🏆 <b>Rang:</b> #{coin_data['market_cap_rank']}
📈 <b>Marktkapitalisierung:</b> ${coin_data['market_cap']:,.0f}
💹 <b>24h Volumen:</b> ${coin_data['volume_24h']:,.0f}

⏰ <i>Aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}</i>
            """
        
        return message
    
    def start_scheduler(self):
        """Запускает планировщик"""
        if not self.scheduler.running:
            self.scheduler.start()
            
            # Восстанавливаем задачи для всех пользователей
            for user_id, notifications in self.user_notifications.items():
                for coin_id, interval in notifications.items():
                    job_id = f"{user_id}_{coin_id}"
                    minutes = TIME_INTERVALS[interval]
                    
                    self.scheduler.add_job(
                        func=self.send_coin_update,
                        trigger='interval',
                        minutes=minutes,
                        args=[user_id, coin_id],
                        id=job_id,
                        replace_existing=True
                    )
    
    def stop_scheduler(self):
        """Останавливает планировщик"""
        if self.scheduler.running:
            self.scheduler.shutdown()

# Глобальная переменная для менеджера уведомлений
notification_manager = None

def init_notification_manager(bot):
    """Инициализирует менеджер уведомлений"""
    global notification_manager
    notification_manager = NotificationManager(bot)
    return notification_manager