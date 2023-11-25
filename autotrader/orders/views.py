from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .api.bybit_api import BybitAPI

@api_view(['GET', 'POST'])
def order_list(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'PUT', 'DELETE', 'POST'])
def order_detail(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        order.delete()
        return Response(status=204)

    elif request.method == 'POST':
        # Ваш код для создания заказа с использованием BybitAPI
        api_key = 'ваш_api_ключ'
        api_secret = 'ваш_api_секрет'
        symbol = 'BTCUSD'

        bybit_api = BybitAPI(api_key, api_secret)

        # Получаем текущую цену для заданного символа
        symbol_price = bybit_api.get_symbol_price(symbol)
        current_price = float(symbol_price['result'][0]['last_price'])

        # Рассчитываем цену покупки
        buy_price_percentage = 1.0 + order.buy_price / 100
        calculated_buy_price = round(current_price * buy_price_percentage, 2)

        # Создаем заказ с рассчитанной ценой покупки
        new_order = Order.objects.create(
            buy_price=calculated_buy_price,
            order_size=order.order_size,
            take_profit_percentage=order.take_profit_percentage,
            stop_loss_percentage=order.stop_loss_percentage
        )

        serializer = OrderSerializer(new_order)
        return Response(serializer.data, status=201)