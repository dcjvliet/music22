import pyaudio
import numpy as np


class Pitch:
    def __init__(self, frequency: float, duration: float, sample_rate: int = 44100, loudness: float = 1):
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

    def cleanup(self):
        if self.audio is not None:
            self.audio.terminate()
