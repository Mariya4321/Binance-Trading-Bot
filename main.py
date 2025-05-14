from binance.client import Client
from binance.enums import *
import logging
import argparse


class BasicBot:
    def __init__(self, apikey, apisecret, testnet=True):
        self.client = Client(apikey, apisecret)
        if testnet:
            self.client.FUTURES_URL = BASE_URL

        logging.basicConfig(
            filename='trading_log.txt',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def place_order(self, symbol, order_type, side, quantity, price=None, stop_price=None):
        try:
            order_params = {
                'symbol': symbol,
                'type': order_type,
                'side': side,
                'quantity': float(quantity),
            }

            if order_type == "LIMIT":
                order_params['price'] = str(price)
                order_params['timeInForce'] = TIME_IN_FORCE_GTC

            elif order_type == "STOP_LIMIT":
                order_params['price'] = str(price)
                order_params['stop_limit'] = str(stop_price)
                order_params['timeInForce'] = TIME_IN_FORCE_GTC

            elif order_type == "OCO":
                order_params['price'] = str(price)
                order_params['stop_limit'] = str(stop_price)
                order_params['limitClientOrderId'] = "uniqueOrderID"
                order_params['timeInForce'] = TIME_IN_FORCE_GTC

            print(order_params)

            order = self.client.futures_create_order(**order_params)
            print("✅ Order placed!")
            print("Order ID:", order['orderId'])
            print("Status:", order['status'])
            print("Symbol:", order['symbol'])
            print("Side:", order['side'])
            print("Type:", order['type'])
            print("Price:", order['price'])
            print("Quantity:", order['origQty'])

            logging.info(f"Order successful: {order}")
        except Exception as e:
            print("❌ Error placing order.")
            print(str(e))
            logging.error(f"Order Failed: {str(e)}")


def Accept_info():
    parser = argparse.ArgumentParser(description="Binance Trading Bot")
    parser.add_argument("symbol", type=str, help="The symbol for the trade (e.g. BTCUSDT)")
    parser.add_argument("order_type", type=str, choices=['LIMIT', 'STOP_LIMIT', 'OCO'], help="Type of the order")
    parser.add_argument("side", type=str, choices=['BUY', 'SELL'], help="Buy or Sell")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders")
    parser.add_argument("--stop_price", type=float, help="Stop price for STOP_LIMIT or OCO orders")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = Accept_info()

    api_key = 'Cr85xFtUiGGTneezj67d6Gkzsf3Av5q1RsAABolWySyXIK9CiAX0RETQo3Zo9Hfp'
    api_secret = 'O4GzO9QhkQhhylmrF3Ydni8qjzyIKMQulWVH887AtBZJWE6w2S1K1f8M73grdfiY'

    BASE_URL = 'https://testnet.binancefuture.com'
    Bot = BasicBot(api_key, api_secret)

    Bot.place_order(args.symbol, args.order_type, args.side, args.quantity, args.price, args.stop_price)
