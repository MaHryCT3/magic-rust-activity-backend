from app.config import logger
from app.repositories.activity_session import ActivitySessionRepository
from app.structs.activity_message import ActivityMessage
from app.structs.activity_session import ActivitySession
from app.structs.enums import ActivityStatus


class ActivityHandler:
    def __init__(self, activity_message: ActivityMessage):
        self.activity_message = activity_message

        self._activity_session_repository = ActivitySessionRepository()

    async def handle(self):
        activity_session = await self._get_or_create_session()

        if self.activity_message.is_sound_muted:
            self._handle_sound_disabled(activity_session)
        else:
            self._handle_sound_enabled(activity_session)

        if not self.activity_message.is_sound_muted and self.activity_message.is_microphone_muted:
            self._handle_microphone_disabled(activity_session)
        else:
            self._handle_microphone_enabled(activity_session)

        activity_session.last_event_at = self.activity_message.datetime

        if self.activity_message.activity_status == ActivityStatus.LEAVE:
            self._handle_leave(activity_session)

        await self._save_session(activity_session)

    async def _get_or_create_session(self):
        if self.activity_message.activity_status == ActivityStatus.JOIN:
            activity_session = self._create_new_session()
        else:
            activity_session = await self._activity_session_repository.get_user_last_activity_session(
                user_id=self.activity_message.user_id,
                start_at_max=self.activity_message.datetime,
                channel_id=self.activity_message.channel_id,
            )

            if not activity_session:
                logger.info(f'Not found active session, for {self.activity_message}, creating new')
                activity_session = self._create_new_session()

        return activity_session

    def _create_new_session(self) -> ActivitySession:
        return ActivitySession(
            user_discord_id=self.activity_message.user_id,
            channel_id=self.activity_message.channel_id,
            channel_type=self.activity_message.channel_type,
            start_at=self.activity_message.datetime,
            last_event_at=self.activity_message.datetime,
        )

    def _handle_microphone_enabled(self, activity_session: ActivitySession):
        if activity_session.is_microphone_mute:
            self._increase_microphone_muted_time(activity_session)
        activity_session.is_microphone_mute = False

    def _handle_microphone_disabled(self, activity_session: ActivitySession):
        if activity_session.is_microphone_mute:
            self._increase_microphone_muted_time(activity_session)
        else:
            activity_session.is_microphone_mute = True

    def _handle_sound_enabled(self, activity_session: ActivitySession):
        if activity_session.is_sound_disabled:
            self._increase_sound_muted_time(activity_session)
        activity_session.is_sound_disabled = False

    def _handle_sound_disabled(self, activity_session: ActivitySession):
        if activity_session.is_sound_disabled:
            self._increase_sound_muted_time(activity_session)
        else:
            activity_session.is_sound_disabled = True

    def _increase_sound_muted_time(self, activity_session: ActivitySession):
        activity_session.sound_disabled_duration += self.activity_message.datetime - activity_session.last_event_at

    def _increase_microphone_muted_time(self, activity_session: ActivitySession):
        print(self.activity_message.datetime, activity_session.last_event_at)
        activity_session.microphone_mute_duration += self.activity_message.datetime - activity_session.last_event_at

    def _handle_leave(self, activity_session: ActivitySession):
        activity_session.end_at = self.activity_message.datetime
        if activity_session.is_microphone_mute:
            self._increase_microphone_muted_time(activity_session)
        if activity_session.is_sound_disabled:
            self._increase_sound_muted_time(activity_session)

    async def _save_session(self, activity_session: ActivitySession):
        if not activity_session.id:
            await self._activity_session_repository.create(activity_session)
        else:
            await self._activity_session_repository.update(activity_session)
