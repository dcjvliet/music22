from python.pitch import Pitch


if __name__ == '__main__':
    # Create a 1 second 440Hz pitch and play it
    pitch = Pitch(frequency=440.0, duration=1.0)
    print(f"Generated {len(pitch.samples)} samples for 440Hz")
    pitch.play()
    pitch.cleanup()

    # Create a 1 second 440Hz pitch and play it at a quarter of the amplitude
    quiet_pitch = Pitch(frequency=440.0, duration=1.0, amplitude=0.25)
    quiet_pitch.play()
    quiet_pitch.cleanup()
