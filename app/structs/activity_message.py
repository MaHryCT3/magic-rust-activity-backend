import datetime
from dataclasses import dataclass

from app.structs.enums import ActivitySessionChannelType, ActivityType


@dataclass(kw_only=True)
class ActivityMessage:
    datetime: datetime.datetime
    user_id: str
    channel_id: str
    channel_type: ActivitySessionChannelType
    activity_type: ActivityType
