import requests
import hashlib
import hmac
import time

class BybitAPI:
    def __init__(self, api_key, api_secret, base_url="https://api.bybit.com"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

    def _generate_signature(self, data):
        ordered_data = dict(sorted(data.items(), key=lambda x: x[0]))
        query_string = '&'.join([f"{k}={v}" for k, v in ordered_data.items()])
        signature = hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        return signature

    def _request(self, method, endpoint, params=None):
        if params is None:
            params = {}

        timestamp = int(time.time() * 1000)
        params['api_key'] = self.api_key
        params['timestamp'] = timestamp

        signature = self._generate_signature(params)
        params['sign'] = signature

        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, params=params)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def get_symbol_price(self, symbol):
        endpoint = "/v2/public/tickers"
        params = {"symbol": symbol}
        return self._request("GET", endpoint, params)

    def create_order(self, symbol, side, quantity, price, order_type="Limit"):
        endpoint = "/v2/private/order/create"
        params = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "order_type": order_type
        }
        return self._request("POST", endpoint, params)