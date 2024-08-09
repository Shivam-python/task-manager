from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return [(tag.value, tag.name.replace("_", " ").title()) for tag in cls]
