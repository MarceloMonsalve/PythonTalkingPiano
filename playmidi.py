import pygame


def play_midi():
    # Initialize and load midi file
    pygame.init()
    midi_file = "talking_piano.mid"
    pygame.mixer.music.load(midi_file)

    # Play MIDI file
    pygame.mixer.music.play()

    # Keep the program running while music plays
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.quit()
