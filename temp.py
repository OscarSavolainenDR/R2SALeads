# Dublin = dict(name='Dublin', country='Ireland', price=50, stripe_subscription_code='price_1MTAETJeYWzBWqCqN7QY44Et'),
Swansea = dict(name='Swansea', country='Wales', price=50, stripe_subscription_code='price_1MaMDnJeYWzBWqCqf0gSXoQi')
Southampton = dict(name='Southampton', country='England', price=50, stripe_subscription_code='price_1MaMDIJeYWzBWqCqBTgxcNBk'),
Plymouth = dict(name='Plymouth', country='England', price=50, stripe_subscription_code='price_1MaMD4JeYWzBWqCqZnfrGMjT'),
Oxford = dict(name='Oxford', country='England', price=50, stripe_subscription_code='price_1MaMCsJeYWzBWqCqNMnEpmct'),
Manchester = dict(name='Manchester', country='England', price=50, stripe_subscription_code='price_1MaMCeJeYWzBWqCqmbfDj3m5'),
London = dict(name='London', country='England', price=200, stripe_subscription_code='price_1MaM7ZJeYWzBWqCqKDTebsJc'),
Liverpool = dict(name='Liverpool', country='England', price=50, stripe_subscription_code='price_1MaMCRJeYWzBWqCqUdiypKw9'),
Glasgow = dict(name='Glasgow', country='Scotland', price=50, stripe_subscription_code='price_1MaMC8JeYWzBWqCqsFn5ptiA'),
Dover = dict(name='Dover', country='England', price=50, stripe_subscription_code='price_1MaMBuJeYWzBWqCqUcJLPoYK'),
Cardiff = dict(name='Cardiff', country='Wales', price=50, stripe_subscription_code='price_1MaMB7JeYWzBWqCqq60ETyIN'),
Cambridge = dict(name='Cambridge', country='England', price=50, stripe_subscription_code='price_1MaMAuJeYWzBWqCqilTOCYSh'),
Bristol = dict(name='Bristol', country='England', price=50, stripe_subscription_code='price_1MaM8dJeYWzBWqCqQTnwoeR7'),
Brighton = dict(name='Brighton', country='England', price=50, stripe_subscription_code='price_1MaMAQJeYWzBWqCqEFyHkScq'),
Bournemouth = dict(name='Bournemouth', country='England', price=50, stripe_subscription_code='price_1MaMACJeYWzBWqCqADuqNDoO'),
Blackpool = dict(name='Blackpool', country='England', price=50, stripe_subscription_code='price_1MaM9uJeYWzBWqCqOXhrrPgM'),
Birmingham = dict(name='Birmingham', country='England', price=50, stripe_subscription_code='price_1MaM9QJeYWzBWqCqxhQoh5A4'),
Bath = dict(name='Bath', country='England', price=50, stripe_subscription_code='price_1MaM8HJeYWzBWqCqAGzDLa8j'),

cities = [
    Bath, Birmingham, Blackpool, Bournemouth, Brighton, Bristol, Cambridge, Cardiff, Dover,
    Glasgow, Liverpool, London, Manchester, Oxford, Plymouth, Southampton, Swansea,
]

for city in cities:
    # try:
    #     city_ = city[0]
    # except:
    # breakpoint()
    if type(city) is tuple:
        city = city[0]
        # print(city)

    print(city['country'])