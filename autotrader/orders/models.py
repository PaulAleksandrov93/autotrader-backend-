from django.db import models
from .api.bybit_api import BybitAPI  # Импортируем наш класс BybitAPI

class Order(models.Model):
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_size = models.IntegerField()
    take_profit_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    stop_loss_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def create_order(self, symbol, side):
        # Здесь вам нужно использовать объект BybitAPI, чтобы создать ордер
        bybit_api = BybitAPI(api_key='ваш_api_key', api_secret='ваш_api_secret')

        # Предположим, что у вас есть значения, которые вы хотите использовать для создания ордера
        quantity = self.order_size
        price = self.buy_price

        # Создаем ордер с помощью метода create_order из класса BybitAPI
        result = bybit_api.create_order(symbol=symbol, side=side, quantity=quantity, price=price)

        # Здесь вы можете добавить дополнительные действия в зависимости от результата создания ордера
        return result