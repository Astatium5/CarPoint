def sort_cars(cars, is_price=False):
    cars_arr: list = []
    price_arr: list = []
    if is_price:
        for car in cars:
            if not car.price in price_arr:
                cars_arr.append(car)
                price_arr.append(car.price)
        return cars_arr
    else:
        return cars