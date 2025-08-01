import aiohttp
import asyncio
import json
from typing import Dict, List, Optional
from config import COINGECKO_API_KEY, BINANCE_API_KEY, BINANCE_SECRET_KEY

class CryptoAPI:
    def __init__(self):
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.binance_base_url = "https://api.binance.com/api/v3"
        self.fear_greed_url = "https://api.alternative.me/fng/"
        
    async def _make_request(self, url: str, params: Dict = None) -> Optional[Dict]:
        """Выполняет HTTP запрос и возвращает JSON данные"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"Error: {response.status} for URL: {url}")
                        return None
        except Exception as e:
            print(f"Request error: {e}")
            return None
    
    async def get_global_metrics(self) -> Optional[Dict]:
        """Получает глобальную метрику криптовалютного рынка"""
        url = f"{self.coingecko_base_url}/global"
        data = await self._make_request(url)
        if data and 'data' in data:
            global_data = data['data']
            return {
                'total_market_cap_usd': global_data.get('total_market_cap', {}).get('usd', 0),
                'total_volume_24h_usd': global_data.get('total_volume', {}).get('usd', 0),
                'market_cap_percentage': global_data.get('market_cap_percentage', {}),
                'active_cryptocurrencies': global_data.get('active_cryptocurrencies', 0),
                'markets': global_data.get('markets', 0),
                'market_cap_change_24h': global_data.get('market_cap_change_percentage_24h_usd', 0)
            }
        return None
    
    async def get_top_coins(self, limit: int = 10) -> Optional[List[Dict]]:
        """Получает топ монет по рыночной капитализации"""
        url = f"{self.coingecko_base_url}/coins/markets"
        params = {
            'vs_currency': 'usd',
            'order': 'market_cap_desc',
            'per_page': limit,
            'page': 1,
            'sparkline': False,
            'price_change_percentage': '24h'
        }
        data = await self._make_request(url, params)
        if data:
            return [{
                'rank': coin['market_cap_rank'],
                'name': coin['name'],
                'symbol': coin['symbol'].upper(),
                'price': coin['current_price'],
                'market_cap': coin['market_cap'],
                'price_change_24h': coin['price_change_percentage_24h'],
                'volume_24h': coin.get('total_volume', 0)
            } for coin in data]
        return None
    
    async def get_binance_top_pairs(self, limit: int = 10) -> Optional[List[Dict]]:
        """Получает топ торговых пар Binance по объему"""
        url = f"{self.binance_base_url}/ticker/24hr"
        data = await self._make_request(url)
        if data:
            # Фильтруем только USDT пары и сортируем по объему
            usdt_pairs = [pair for pair in data if pair['symbol'].endswith('USDT')]
            sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x['quoteVolume']), reverse=True)
            
            return [{
                'symbol': pair['symbol'],
                'price': float(pair['lastPrice']),
                'price_change_24h': float(pair['priceChangePercent']),
                'volume_24h': float(pair['quoteVolume']),
                'high_24h': float(pair['highPrice']),
                'low_24h': float(pair['lowPrice'])
            } for pair in sorted_pairs[:limit]]
        return None
    
    async def get_fear_greed_index(self) -> Optional[Dict]:
        """Получает индекс страха и жадности"""
        data = await self._make_request(self.fear_greed_url)
        if data and 'data' in data and len(data['data']) > 0:
            index_data = data['data'][0]
            value = int(index_data['value'])
            
            # Определяем статус на основе значения
            if value <= 25:
                status = "Extreme Fear"
                emoji = "😱"
            elif value <= 45:
                status = "Fear"
                emoji = "😰"
            elif value <= 55:
                status = "Neutral"
                emoji = "😐"
            elif value <= 75:
                status = "Greed"
                emoji = "🤑"
            else:
                status = "Extreme Greed"
                emoji = "🤑🤑"
            
            return {
                'value': value,
                'value_classification': index_data['value_classification'],
                'status': status,
                'emoji': emoji,
                'timestamp': index_data['timestamp']
            }
        return None
    
    async def get_trending_coins(self) -> Optional[List[Dict]]:
        """Получает трендовые монеты"""
        url = f"{self.coingecko_base_url}/search/trending"
        data = await self._make_request(url)
        if data and 'coins' in data:
            return [{
                'name': coin['item']['name'],
                'symbol': coin['item']['symbol'],
                'market_cap_rank': coin['item']['market_cap_rank'],
                'price_btc': coin['item']['price_btc']
            } for coin in data['coins']]
        return None
    
    async def get_defi_metrics(self) -> Optional[Dict]:
        """Получает DeFi метрики"""
        url = f"{self.coingecko_base_url}/global/decentralized_finance_defi"
        data = await self._make_request(url)
        if data and 'data' in data:
            defi_data = data['data']
            return {
                'defi_market_cap': defi_data.get('defi_market_cap', 0),
                'eth_market_cap': defi_data.get('eth_market_cap', 0),
                'defi_to_eth_ratio': defi_data.get('defi_to_eth_ratio', 0),
                'trading_volume_24h': defi_data.get('trading_volume_24h', 0),
                'defi_dominance': defi_data.get('defi_dominance', 0),
                'top_coin_name': defi_data.get('top_coin_name', ''),
                'top_coin_defi_dominance': defi_data.get('top_coin_defi_dominance', 0)
            }
        return None
    
    async def get_coin_info(self, coin_id: str) -> Optional[Dict]:
        """Получает информацию о конкретной монете"""
        url = f"{self.coingecko_base_url}/coins/{coin_id}"
        params = {
            'localization': False,
            'tickers': False,
            'market_data': True,
            'community_data': False,
            'developer_data': False,
            'sparkline': False
        }
        data = await self._make_request(url, params)
        if data and 'market_data' in data:
            market_data = data['market_data']
            return {
                'name': data['name'],
                'symbol': data['symbol'].upper(),
                'current_price': market_data['current_price']['usd'],
                'market_cap': market_data['market_cap']['usd'],
                'price_change_24h': market_data['price_change_percentage_24h'],
                'price_change_7d': market_data['price_change_percentage_7d'],
                'volume_24h': market_data['total_volume']['usd'],
                'market_cap_rank': market_data['market_cap_rank']
            }
        return None

# Создаем глобальный экземпляр API
crypto_api = CryptoAPI()