from dataclasses import dataclass

import assemblyai as aai

from app.services.voices_records.craig_download import CraigTrack
from core.actions.abstract import AbstractAction


@dataclass
class TranscriptAudioAction(AbstractAction[str]):
    audio_path: str
    tracks_info: list[CraigTrack]

    async def action(self) -> str:
        transcribe_result = aai.Transcriber().transcribe(
            self.audio_path,
            config=aai.TranscriptionConfig(
                multichannel=True,
                language_code='ru',
            ),
        )
        return self._format_transcript(transcribe_result)

    def _format_transcript(self, transcript: aai.Transcript) -> str:
        sentences = transcript.get_sentences()
        full_text = ''
        speaker_text = ''
        for current_sentence, next_sentence in zip(sentences, sentences[1:]):
            current_sentence: aai.Sentence
            next_sentence: aai.Sentence

            speaker_text += f' {current_sentence.text}'
            if next_sentence.speaker == current_sentence.speaker:
                continue
            else:
                speaker_label = self._get_speaker_label(int(current_sentence.speaker))
                full_text += f'{speaker_label}: {speaker_text} \n'
                speaker_text = ''

        return full_text

    def _get_speaker_label(self, label: int) -> str:
        return self.tracks_info[label - 1].user_name
