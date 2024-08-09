from enum import Enum

ALLOWED_IS_ACTIVE = ['1', '0', 1, 0]


class DateEnums(Enum):
    DATE_FORMAT = '%Y-%m-%d'
    DATE_FORMAT_WITH_TIME = "%Y-%m-%d %H:%M:%S"
    DATE_FORMAT_WITH_TIME_V1 = "%d-%m-%Y %H:%I:%S"
