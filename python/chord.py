import numpy as np
import pyaudio

from .note import Note


class Chord:
    def __init__(self, notes: list[Note]):
        """Initializes a Chord object

        :param notes: The list of Note objects that make up the chord
        :type notes: list[Note]
        :raises ValueError: If no notes are provided
        """
        if not notes or len(notes) == 0:
            raise ValueError('At least one note is required to create a chord')
        
        self.notes = notes
        self.audio = None
        self.mixed = None
        self.sample_rate = None

    def _mix_samples(self):
        """Mix the frequencies of the individual notes to create the chord sound
        """
        # this is essentially the same logic as for note, but now with notes instead of pitches
        for note in self.notes:
            if note.mixed is None:
                note._mix_samples()
        
        max_duration = max(len(note.mixed) / note.sample_rate for note in self.notes) # type: ignore
        sample_rate = min(note.sample_rate for note in self.notes) # type: ignore

        mixed = np.zeros(int(sample_rate * max_duration), dtype=np.float32)

        for note in self.notes:
            samples = note.mixed 
            if len(samples) < len(mixed): # type: ignore
                samples = np.pad(samples, (0, len(mixed) - len(samples)), mode='constant') # type: ignore
            
            mixed += samples[:len(mixed)] # type: ignore

        # Normalize to prevent clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val

        # store so we only have to do this once
        self.mixed = mixed
        self.sample_rate = sample_rate

    def play(self):
        """Play the chord
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
        """Save the chord to an output file

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
        """Delete the PyAudio instance if the chord is no longer needed
        """
        if self.audio is not None:
            self.audio.terminate()
