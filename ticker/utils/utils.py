from enum import IntEnum


class UserTier(IntEnum):
    NORMAL = 1
    PREMIUM = 2
    GOLD = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


def getPeriodTimeDelta(duration):
    period = "1M"
    deltaD = 0  # refers to historical days to revind from
    if duration == "5D":
        period = "5M"
        deltaD = 7
    elif duration == "1M":
        period = "1H"
        deltaD = 26
    elif duration == "6M":
        period = "1D"
        deltaD = 6*26
    elif duration == "1Y":
        period = "1D"
        deltaD = 12*26
    elif duration == "5Y":
        period = "1W"
        deltaD = 60 * 26
    return period, deltaD
