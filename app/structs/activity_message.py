import datetime
from dataclasses import dataclass

from app.structs.enums import ActivitySessionChannelType, ActivityStatus


@dataclass(kw_only=True)
class ActivityMessage:
    datetime: datetime.datetime
    user_id: str
    channel_id: str
    channel_type: ActivitySessionChannelType
    activity_status: ActivityStatus
    is_microphone_muted: bool
    is_sound_muted: bool
