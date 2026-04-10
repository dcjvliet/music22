from python.pitch import Pitch


if __name__ == '__main__':
    # Test the Pitch class
    pitch = Pitch(frequency=440.0, duration=2.0)
    print(f"Generated {len(pitch.samples)} samples for 440Hz")
    pitch.play()
    pitch.cleanup()
