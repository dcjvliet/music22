import pyaudio
import numpy as np


class Pitch:
    def __init__(self, pitch: float, duration: float, sample_rate: int = 44100):
        self.pitch = pitch
        self.duration = duration
        self.sample_rate = sample_rate
        self.audio = pyaudio.PyAudio()

        # generate samples required to play the pitch
        self.samples = (np.sin(2 * np.pi * np.arange(self.sample_rate * self.duration) * self.pitch / self.sample_rate)).astype(np.float32)

    def play(self):
        stream = self.audio.open(format=pyaudio.paFloat32,
                                 channels=1,
                                 rate=self.sample_rate,
                                 output=True)
        
        stream.write(self.samples.tobytes())

        stream.stop_stream()
        stream.close()

    def cleanup(self):
        self.audio.terminate()
