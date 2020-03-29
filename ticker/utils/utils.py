from enum import IntEnum


class UserTier(IntEnum):
    NORMAL = 1
    PREMIUM = 2
    GOLD = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]
