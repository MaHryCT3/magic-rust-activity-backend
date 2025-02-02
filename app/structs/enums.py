from enum import StrEnum


class ActivitySessionChannelType(StrEnum):
    VOICE = 'VOICE'
    STAGE = 'STAGE'
    USER_ROOM = 'USER_ROOM'


class ActivityType(StrEnum):
    JOIN = 'JOIN'
    LEAVE = 'LEAVE'
    ACTIVE = 'ACTIVE'
    DISABLE_MICROPHONE = 'DISABLE_MICROPHONE'
    ENABLE_MICROPHONE = 'ENABLE_MICROPHONE'
    MICROPHONE_DISABLED = 'MICROPHONE_DISABLED'  # событие о том что микрофон все еще выключен
    DISABLE_SOUND = 'DISABLE_SOUND'
    ENABLE_SOUND = 'ENABLE_SOUND'
    SOUND_DISABLED = 'SOUND_DISABLED'  # по анологии с микрофоном
