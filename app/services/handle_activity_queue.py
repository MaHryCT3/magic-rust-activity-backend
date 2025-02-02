from app.config import logger
from app.repositories.activity_session import ActivitySessionRepository
from app.structs.activity_message import ActivityMessage
from app.structs.activity_session import ActivitySession
from app.structs.enums import ActivityType


class ActivityHandler:
    def __init__(self, activity_message: ActivityMessage):
        self.activity_message = activity_message

        self._activity_session_repository = ActivitySessionRepository()

    async def handle(self):  # noqa: PLR0912
        if self.activity_message.activity_type == ActivityType.JOIN:
            activity_session = self._create_new_session()
        else:
            activity_session = await self._activity_session_repository.get_user_last_activity_session(
                user_id=self.activity_message.user_id,
            )

            if not activity_session:
                logger.warning(f'Not found active session, for {self.activity_message}, creating new')
                activity_session = self._create_new_session()

        match self.activity_message.activity_type:
            case ActivityType.LEAVE:
                activity_session.end_at = self.activity_message.datetime
                if activity_session.is_microphone_mute:
                    self._increase_microphone_muted_time(activity_session)
                if activity_session.is_sound_disabled:
                    self._increase_sound_muted_time(activity_session)

            case ActivityType.DISABLE_MICROPHONE:
                activity_session.is_microphone_mute = True

            case ActivityType.ENABLE_MICROPHONE:
                activity_session.is_microphone_mute = False
                self._increase_microphone_muted_time(activity_session)

            case ActivityType.MICROPHONE_DISABLED:
                activity_session.is_microphone_mute = True
                self._increase_microphone_muted_time(activity_session)

            case ActivityType.DISABLE_SOUND:
                activity_session.is_sound_disabled = True
                activity_session.is_microphone_mute = False

            case ActivityType.ENABLE_SOUND:
                activity_session.is_sound_disabled = False
                self._increase_sound_muted_time(activity_session)

            case ActivityType.SOUND_DISABLED:
                activity_session.is_sound_disabled = True
                activity_session.is_microphone_mute = False
                self._increase_sound_muted_time(activity_session)

        activity_session.last_event_at = self.activity_message.datetime
        await self._save_session(activity_session)

    def _create_new_session(self) -> ActivitySession:
        return ActivitySession(
            user_discord_id=self.activity_message.user_id,
            channel_id=self.activity_message.channel_id,
            channel_type=self.activity_message.channel_type,
            start_at=self.activity_message.datetime,
            last_event_at=self.activity_message.datetime,
        )

    def _increase_sound_muted_time(self, activity_session: ActivitySession):
        activity_session.sound_disabled_duration += self.activity_message.datetime - activity_session.last_event_at

    def _increase_microphone_muted_time(self, activity_session: ActivitySession):
        activity_session.microphone_mute_duration += self.activity_message.datetime - activity_session.last_event_at

    async def _save_session(self, activity_session: ActivitySession):
        if not activity_session.id:
            await self._activity_session_repository.create(activity_session)
        else:
            await self._activity_session_repository.update(activity_session)
