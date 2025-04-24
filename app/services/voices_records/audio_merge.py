import os
import subprocess
from dataclasses import dataclass
from typing import ClassVar

from core.actions.abstract import AbstractAction


@dataclass
class AudioMergeAction(AbstractAction[list[str]]):
    voices_paths: list[str]
    output_dir: str

    SAMPLE_RATE: ClassVar[int] = 44100
    BIT_DEPTH: ClassVar[int] = 16
    CHUNK_SIZE_MB: ClassVar[int] = 400

    @property
    def temp_dir(self):
        return f'{self.output_dir}/tmp'

    async def action(self) -> list[str]:
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        max_duration = self._find_max_tracks_max_duration()
        equalized_tracks_paths = self._equalize_tracks(max_duration)
        wv_path = self._merge_and_convert_to_wavpack(equalized_tracks_paths)
        chunk_paths = self._split_into_chunks(wv_path, len(equalized_tracks_paths))

        return chunk_paths

    def _find_max_tracks_max_duration(self):
        max_duration = 0
        for path in self.voices_paths:
            result = subprocess.run(
                [
                    'ffprobe',
                    '-v',
                    'error',
                    '-show_entries',
                    'format=duration',
                    '-of',
                    'default=noprint_wrappers=1:nokey=1',
                    path,
                ],
                capture_output=True,
                text=True,
            )

            duration = float(result.stdout.strip())
            max_duration = max(max_duration, duration)
        return max_duration

    def _equalize_tracks(self, duration: float):
        padded_paths = []
        for i, file in enumerate(self.voices_paths):
            out_path = os.path.join(self.temp_dir, f'padded_{i:03}.wav')
            padded_paths.append(out_path)

            subprocess.run(
                [
                    'ffmpeg',
                    '-y',
                    '-i',
                    file,
                    '-af',
                    f'apad=pad_dur={duration}',
                    '-t',
                    str(duration),
                    '-ac',
                    '1',
                    '-ar',
                    str(self.SAMPLE_RATE),
                    '-sample_fmt',
                    's16',
                    '-c:a',
                    'pcm_s16le',
                    out_path,
                ],
                check=True,
            )
        return padded_paths

    def _merge_and_convert_to_wavpack(self, padded_paths: list[str]) -> str:
        inputs = []
        amerge_inputs = []

        for i, path in enumerate(padded_paths):
            inputs.extend(['-i', path])
            amerge_inputs.append(f'[{i}:a]')

        filter_complex = ''.join(amerge_inputs) + f'amerge=inputs={len(padded_paths)}[aout]'
        wv_path = os.path.join(self.output_dir, 'merged.wv')

        subprocess.run(
            [
                'ffmpeg',
                *inputs,
                '-filter_complex',
                filter_complex,
                '-map',
                '[aout]',
                '-ac',
                str(len(padded_paths)),
                '-ar',
                str(self.SAMPLE_RATE),
                '-c:a',
                'wavpack',
                '-y',
                wv_path,
            ],
            check=True,
        )

        return wv_path

    def _split_into_chunks(self, input_path: str, num_channels: int) -> list[str]:
        segment_prefix = os.path.join(self.output_dir, 'chunk_%03d.wv')
        segment_time = self._estimate_segment_time(self.CHUNK_SIZE_MB, self.SAMPLE_RATE, self.BIT_DEPTH, num_channels)

        subprocess.run(
            [
                'ffmpeg',
                '-i',
                input_path,
                '-f',
                'segment',
                '-segment_time',
                str(segment_time),
                '-c',
                'copy',
                '-map',
                '0',
                '-y',
                segment_prefix,
            ],
            check=True,
        )

        # Получаем список всех chunk-файлов
        chunk_paths = sorted(
            [
                os.path.join(self.output_dir, f)
                for f in os.listdir(self.output_dir)
                if f.startswith('chunk_') and f.endswith('.wv')
            ]
        )

        return chunk_paths

    def _estimate_segment_time(self, target_mb: int, sr: int, bit_depth: int, channels: int) -> int:
        bytes_per_sec = sr * (bit_depth / 8) * channels
        return int((target_mb * 1024 * 1024) / bytes_per_sec)
