import datetime
from typing import Callable


def get_default_datetime_factory(timezone: datetime.timezone | None = None) -> Callable[[], datetime.datetime]:
    def default_datetime_factory():
        return datetime.datetime.now(tz=timezone)

    return default_datetime_factory
