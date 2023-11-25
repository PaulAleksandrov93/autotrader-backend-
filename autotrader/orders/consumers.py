import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from api.bybit_api import BybitAPI

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'set_order_parameters':
            # Получаем параметры из утилиты
            price_percentage = float(text_data_json['price_percentage'])
            take_profit_parameters = text_data_json['take_profit_parameters']
            stop_loss_parameters = text_data_json['stop_loss_parameters']

            # Вычисляем цену покупки (пример)
            current_price = 100  # Замените это на получение текущей цены откуда-то
            buy_price = current_price * (1 + price_percentage / 100)

            # Вызываем функцию apply_order_parameters
            await self.apply_order_parameters(buy_price, take_profit_parameters, stop_loss_parameters)

            # Отправляем подтверждение клиенту
            await self.send(text_data=json.dumps({
                'action': 'order_parameters_set',
                'status': 'success',
            }))
        elif action == 'other_action':
            # Добавьте другие действия, если необходимо
            pass

    async def apply_order_parameters(self, buy_price, take_profit_parameters, stop_loss_parameters):
        # Получаем API ключи из секретного хранилища (вам нужно реализовать свой механизм)
        api_key = "ваш_api_key"
        api_secret = "ваш_api_secret"

        # Создаем экземпляр BybitAPI
        bybit_api = BybitAPI(api_key=api_key, api_secret=api_secret)

        # Параметры ордера
        symbol = "BTCUSD"  # Замените на торговый символ, который вы используете
        order_quantity = 1  # Вы можете настроить количество в соответствии с вашими требованиями
        order_type = "Limit"  # Используйте "Limit" для ордера по определенной цене

        # Вычисляем take profit и stop loss
        take_profit_type, take_profit_value = take_profit_parameters.split(':')
        stop_loss_type, stop_loss_value = stop_loss_parameters.split(':')

        if take_profit_type == 'roi':
            take_profit = buy_price * (1 + float(take_profit_value) / 100)
        elif take_profit_type == 'price_change':
            take_profit = buy_price + float(take_profit_value)
        else:
            raise ValueError(f"Unsupported take profit type: {take_profit_type}")

        if stop_loss_type == 'roi':
            stop_loss = buy_price * (1 - float(stop_loss_value) / 100)
        elif stop_loss_type == 'price_change':
            stop_loss = buy_price - float(stop_loss_value)
        else:
            raise ValueError(f"Unsupported stop loss type: {stop_loss_type}")

        # Выставляем ордер на покупку
        bybit_api.place_order(symbol, "Buy", order_quantity, buy_price, order_type)

        # Выставляем ордер на Take Profit
        bybit_api.place_order(symbol, "Sell", order_quantity, take_profit, order_type)

        # Выставляем ордер на Stop Loss
        bybit_api.place_order(symbol, "Sell", order_quantity, stop_loss, order_type)