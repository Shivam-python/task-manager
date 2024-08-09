from task_management.utils.enum_utility import BaseEnum


class PriorityEnum(BaseEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'


class EnvironmentEnum(BaseEnum):
    NOT_STARTED = 'not_started'
    DEV = 'dev'
    UAT = 'uat'
    STAGING = 'staging'
    PREPROD = 'preprod'
    PRODUCTION = 'production'


class StatusEnum(BaseEnum):
    NOT_STARTED = 'not_started'
    IN_PROGRESS = 'in_progress'
    NEEDS_REVIEW = 'needs_review'
    COMPLETED = 'completed'
