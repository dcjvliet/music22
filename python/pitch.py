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
        if not self.frequency or self.frequency <= 0:
            raise ValueError('Frequency must be a positive number')
        if not self.duration or self.duration <= 0:
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

    def cleanup(self):
        """Delete the PyAudio instance if the pitch is no longer needed
        """
        if self.audio is not None:
            self.audio.terminate()
