import math


def convert_price(price, to_currency, from_currency):
    return math.ceil(price * from_currency.rate / to_currency.rate)


def get_delivery_price(price, currency):
    usd_price = math.ceil(price * currency.rate)
    delivery_price = 0
    if usd_price < 2000:
        delivery_price = 350
    elif usd_price > 35000:
        delivery_price = 2500
    return math.ceil(delivery_price / currency.rate)
