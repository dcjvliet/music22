import pyaudio
import numpy as np

from .pitch import Pitch


class Note:
    def __init__(self, pitches: list[Pitch]):
        """Initializes a Note object

        :param pitches: A list of Pitch objects that make up the note
        :type pitches: list[Pitch]
        :raises ValueError: If no pitches are provided
        """
        if not pitches or len(pitches) == 0:
            raise ValueError('At least one pitch is required to create a note')
        
        self.pitches = pitches
        self.audio = None
        self.mixed = None
        self.sample_rate = None

    def _mix_samples(self):
        """Mix the samples of the notes individual pitches together
        """
        max_duration = max(pitch.duration for pitch in self.pitches) # Find the maximum duration
        sample_rate = min(pitch.sample_rate for pitch in self.pitches) # Use the lowest sample rate among pitches
        
        total_samples = int(sample_rate * max_duration)
        
        mixed = np.zeros(total_samples, dtype=np.float32)
        
        for pitch in self.pitches:
            samples = pitch.samples
            # Pad with zeros if this pitch is shorter than max duration
            if len(samples) < total_samples:
                samples = np.pad(samples, (0, total_samples - len(samples)), mode='constant')
            # Add to mixed (take only the amount we need)
            mixed += samples[:total_samples]
        
        # Normalize to prevent clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val

        # store so we only have to do this once
        self.mixed = mixed
        self.sample_rate = sample_rate

    def play(self):
        """Play the note
        """
        if self.mixed is None or self.sample_rate is None:
            self._mix_samples()

        if self.audio is None:
            # create if needed
            self.audio = pyaudio.PyAudio()

        # Play the mixed audio
        stream = self.audio.open(format=pyaudio.paFloat32,
                           channels=1,
                           rate=self.sample_rate, # type: ignore
                           output=True)
        stream.write(self.mixed.tobytes()) # type: ignore
        stream.stop_stream()
        stream.close()

    def save_to_file(self, file_type: str, output_path: str):
        """Save the note to an output file

        :param file_type: The file extension
        :type file_type: str
        :param output_path: The output file path
        :type output_path: str
        :raises ValueError: If file_type is not specified
        :raises ValueError: If output_path is not specified
        :raises ValueError: If file_type is not supported
        """
        # make necessary imports only if we need to
        import os
        import wave
        from pydub import AudioSegment

        if not file_type:
            raise ValueError("file_type is required.")
        if not output_path:
            raise ValueError("output_path is required.")

        # mix samples if we haven't played the note yet
        if self.mixed is None or self.sample_rate is None:
            self._mix_samples()

        filetype = file_type.lower().lstrip('.')

        # Add or replace extension to match requested output type.
        root, _ext = os.path.splitext(output_path)
        final_path = root + f".{filetype}"

        out_dir = os.path.dirname(final_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        pcm = np.clip(self.mixed, -1.0, 1.0) # type: ignore
        pcm16 = (pcm * 32767).astype(np.int16)

        if filetype == 'wav':
            with wave.open(final_path, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate) # type: ignore
                wf.writeframes(pcm16.tobytes())
            return

        # For compressed formats, export through ffmpeg via pydub.
        supported_ffmpeg_formats = {
            'mp3', 'flac', 'ogg', 'aac', 'm4a', 'wma', 'aiff', 'opus', 'webm'
        }
        if filetype not in supported_ffmpeg_formats:
            supported = ', '.join(sorted({'wav', *supported_ffmpeg_formats}))
            raise ValueError(f"Unsupported file type '{filetype}'. Supported types: {supported}")

        segment = AudioSegment(
            data=pcm16.tobytes(),
            sample_width=2,
            frame_rate=self.sample_rate, # type: ignore
            channels=1,
        )
        segment.export(final_path, format=filetype)

    def cleanup(self):
        """Delete the PyAudio instance if the note is no longer needed
        """
        if self.audio is not None:
            self.audio.terminate()
