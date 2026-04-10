import pyaudio
import numpy as np

from .pitch import Pitch


class Note:
    def __init__(self, pitches: list[Pitch]):
        self.pitches = pitches
        self.audio = None

    def play(self):
        if not self.pitches or len(self.pitches) == 0:
            return
        
        if self.audio is None:
            # create if needed
            self.audio = pyaudio.PyAudio()

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
        
        # Play the mixed audio
        stream = self.audio.open(format=pyaudio.paFloat32,
                           channels=1,
                           rate=sample_rate,
                           output=True)
        stream.write(mixed.tobytes())
        stream.stop_stream()
        stream.close()

    def cleanup(self):
        if self.audio is not None:
            self.audio.terminate()
