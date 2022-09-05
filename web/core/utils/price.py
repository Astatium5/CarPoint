def set_min_price(dct_cars):
    for k, v in dct_cars.items():
        min_price = min([k["price"] for k in v["pattern"]])
        dct_cars[k]["min_price"] = min_price
    return dct_cars


def increase_price(min: float) -> list:
    min: int = int(min) - 500000
    max: int = int(min) + 300000
    return [min, max]
