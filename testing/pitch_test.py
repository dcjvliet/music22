from python.pitch import Pitch


if __name__ == '__main__':
    # Create a 1 second 440Hz pitch and play it
    pitch = Pitch(frequency=440.0, duration=1, loudness=0.5)
    print(f"Generated {len(pitch.samples)} samples for 440Hz")
    pitch.play()
    pitch.cleanup()

    # Create a 1 second 440Hz pitch and play it at a quarter of the amplitude
    quiet_pitch = Pitch(frequency=440.0, duration=1.0, loudness=1)
    quiet_pitch.play()
    quiet_pitch.save_to_file('wav', 'quiet_pitch.wav')
    quiet_pitch.save_to_file('ogg', 'quiet_pitch.ogg')
    quiet_pitch.save_to_file('mp3', 'quiet_pitch')
    quiet_pitch.cleanup()
