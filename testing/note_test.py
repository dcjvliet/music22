from python.note import Note
from python.pitch import Pitch


if __name__ == '__main__':
    # harmonics for C4 roughly (amplitudes complete guess)
    harmonic_1 = Pitch(261.63, 1, amplitude=1)
    harmonic_2 = Pitch(523.26, 1, amplitude=0.5)
    harmonic_3 = Pitch(784.89, 1, amplitude=0.25)
    harmonic_4 = Pitch(1046.52, 1, amplitude=0.125)
    harmonic_5 = Pitch(1308.15, 1, amplitude=0.0625)

    # create the C4 note and play it
    c4_note = Note([harmonic_1, harmonic_2, harmonic_3, harmonic_4, harmonic_5])
    c4_note.play()
    c4_note.cleanup()

    # change harmonic 1 to not last as long
    harmonic_1 = Pitch(261.63, 0.25, amplitude=1)
    c4_note = Note([harmonic_1, harmonic_2, harmonic_3, harmonic_4, harmonic_5])
    c4_note.play()
    c4_note.cleanup()
