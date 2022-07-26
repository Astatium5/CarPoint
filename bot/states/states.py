from dataclasses import dataclass

from aiogram.dispatcher.filters.state import StatesGroup, State


class Meeting(StatesGroup):
    name = State()
    city = State()


class ReceiveOffer(StatesGroup):
    phone = State()
    phone_string = State()


class Volume(StatesGroup):
    min = State()
    max = State()


class Power(StatesGroup):
    min = State()
    max = State()


class Price(StatesGroup):
    min = State()
    max = State()
    specific_amount = State()


@dataclass
class OfferMetaData:
    # Price
    MinPrice: int
    MaxPrice: int

    # Marks
    IsAnyMark: bool
    Mark: str

    # Body
    Body: str

    # Fuel type
    IsAnyFuelType: bool
    FuelType: str

    # Volume or power
    IsVolume: bool
    IsPower: bool

    MinVolume: float
    MaxVolume: float

    MinPower: int
    MaxPower: int

    # Transmission
    Transmission: str


    def __init__(self,
        MinPrice=0, MaxPrice=0,
        IsAnyMark=False, Mark="", Body="", IsAnyFuelType=False, FuelType="",
        IsVolume=False, IsPower=False, MinVolume=0.0, MaxVolume=0.0, MinPower=0, MaxPower=0,
        Transmission=""
    ):

        self.MinPrice = MinPrice
        self.MaxPrice = MaxPrice

        self.IsAnyMark = IsAnyMark
        self.Mark = Mark

        self.Body = Body

        self.IsAnyFuelType = IsAnyFuelType
        self.FuelType = FuelType

        self.IsVolume = IsVolume
        self.IsPower = IsPower

        self.MinVolume = MinVolume
        self.MaxVolume = MaxVolume

        self.MinPower = MinPower
        self.MaxPower = MaxPower

        self.Transmission = Transmission


    def to_header(self):
        return {"Min-Price": self.MinPrice, "Max-Price": self.MaxPrice, "Is-Any-Fuel-Type": self.IsAnyFuelType,
                "Is-Any-Mark": self.IsAnyMark, "Mark": self.Mark, "Is-Volume": self.IsVolume,
                "Is-Power": self.IsPower, "Min-Volume": self.MinVolume, "Max-Volume": self.MaxVolume,
                "Min-Power": self.MinPower, "Max-Power": self.MaxPower}
