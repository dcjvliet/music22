import pyaudio
import numpy as np


class Pitch:
    def __init__(self, frequency: float, duration: float, sample_rate: int = 44100, loudness: float = 1):
        """Initialize the pitch object

        :param frequency: The frequency of the pitch in Hz
        :type frequency: float
        :param duration: The duration of the pitch in seconds
        :type duration: float
        :param sample_rate: The sample rate for the audio, defaults to 44100
        :type sample_rate: int, optional
        :param loudness: The loudness of the pitch, defaults to 1
        :type loudness: float, optional
        :raises ValueError: If frequency is not a positive number
        :raises ValueError: If duration is not a positive number
        :raises ValueError: If loudness is not in the interval [0, 1]
        """
        if not frequency or frequency <= 0:
            raise ValueError('Frequency must be a positive number')
        if not duration or duration <= 0:
            raise ValueError('Duration must be a positive number')
        
        self.frequency = frequency
        self.duration = duration
        self.sample_rate = sample_rate
        if loudness < 0 or loudness > 1:
            raise ValueError('Loudness must be between 0 and 1')
        
        self.loudness = loudness ** 1.66 # roughly account for how loud something sounds to humans
        self.audio = None

        # generate samples required to play the pitch
        self.samples = (self.loudness * np.sin(2 * np.pi * np.arange(self.sample_rate * self.duration) * self.frequency / self.sample_rate)).astype(np.float32)

    def play(self):
        """Play the pitch
        """
        # create audio if necessary
        if self.audio is None:
            self.audio = pyaudio.PyAudio()

        stream = self.audio.open(format=pyaudio.paFloat32,
                                 channels=1,
                                 rate=self.sample_rate,
                                 output=True)
        
        stream.write(self.samples.tobytes())

        stream.stop_stream()
        stream.close()

    def save_to_file(self, file_type: str, output_path: str):
        # make necessary imports only if we need to
        import os
        import wave
        from pydub import AudioSegment

        if not file_type:
            raise ValueError("file_type is required.")
        if not output_path:
            raise ValueError("output_path is required.")

        filetype = file_type.lower().lstrip('.')

        # Add or replace extension to match requested output type.
        root, _ext = os.path.splitext(output_path)
        final_path = root + f".{filetype}"

        out_dir = os.path.dirname(final_path)
        if out_dir:
            os.makedirs(out_dir, exist_ok=True)

        pcm = np.clip(self.samples, -1.0, 1.0) # type: ignore
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
        """Delete the PyAudio instance if the pitch is no longer needed
        """
        if self.audio is not None:
            self.audio.terminate()
