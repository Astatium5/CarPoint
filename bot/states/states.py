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
    # User Id
    UserId: int

    # Price
    IsRange: bool
    IsMyselfRange: bool
    IsSpecificAmount: bool

    RangeId: str
    MinPrice: int
    MaxPrice: int
    SpecificPriceAmount: int

    # Marks
    IsAnyMark: bool
    Mark: str

    # Body
    Body: str

    # Fuel type
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
        UserId=0, IsRange=False, IsMyselfRange=False, IsSpecificAmount=False,
        RangeId="", MinPrice=0, MaxPrice=0, SpecificPriceAmount=0,
        IsAnyMark=False, Mark="", Body="", FuelType="",
        IsVolume=False, IsPower=False, MinVolume=0.0, MaxVolume=0.0, MinPower=0, MaxPower=0,
        Transmission=""
    ):
        self.UserId = UserId
        self.IsRange = IsRange
        self.IsMyselfRange = IsMyselfRange
        self.IsSpecificAmount = IsSpecificAmount

        self.RangeId = RangeId
        self.MinPrice = MinPrice
        self.MaxPrice = MaxPrice
        self.SpecificPriceAmount = SpecificPriceAmount

        self.IsAnyMark = IsAnyMark
        self.Mark = Mark

        self.Body = Body

        self.FuelType = FuelType

        self.IsVolume = IsVolume
        self.IsPower = IsPower
        self.MinVolume = MinVolume
        self.MaxVolume = MaxVolume
        self.MinPower = MinPower
        self.MaxPower = MaxPower

        self.transmission = Transmission
