from enum import StrEnum


class ActivitySessionChannelType(StrEnum):
    VOICE = 'VOICE'
    STAGE = 'STAGE'
    USER_ROOM = 'USER_ROOM'


class ActivityStatus(StrEnum):
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'
    ACTIVE = 'ACTIVE'
