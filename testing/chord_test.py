from python.note import Note
from python.pitch import Pitch
from python.chord import Chord


if __name__ == '__main__':
    # create some notes
    c4_note = Note([
        Pitch(261.63, 2, loudness=1),
        Pitch(523.26, 2, loudness=0.5),
        Pitch(784.89, 2, loudness=0.25),
        Pitch(1046.52, 2, loudness=0.125),
        Pitch(1308.15, 2, loudness=0.0625)
    ])

    e4_note = Note([
        Pitch(329.63, 2, loudness=1),
        Pitch(659.26, 2, loudness=0.5),
        Pitch(988.89, 2, loudness=0.25),
        Pitch(1318.52, 2, loudness=0.125),
        Pitch(1653.15, 2, loudness=0.0625)
    ])

    g4_note = Note([
        Pitch(392.00, 2, loudness=1),
        Pitch(783.99, 2, loudness=0.5),
        Pitch(1175.99, 2, loudness=0.25),
        Pitch(1567.98, 2, loudness=0.125),
        Pitch(1963.99, 2, loudness=0.0625)
    ])

    # drop the b flat to go from C7 -> Cmaj
    bflat4_note = Note([
        Pitch(466.16, 1, loudness=1),
        Pitch(932.33, 1, loudness=0.5),
        Pitch(1398.49, 1, loudness=0.25),
        Pitch(1864.66, 1, loudness=0.125),
        Pitch(2796.92, 1, loudness=0.0625)
    ])

    # create a C major chord and play it
    c_major_chord = Chord([c4_note, e4_note, g4_note, bflat4_note])
    c_major_chord.play()
    c_major_chord.save_to_file('wav', 'c_major_chord.wav')
    c_major_chord.save_to_file('mp3', 'c_major_chord')
    c_major_chord.cleanup()
