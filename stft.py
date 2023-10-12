from midiutil import MIDIFile
import librosa
import numpy as np


def create_midi():
    # Load the audio file
    audio_path = "recording.wav"
    y, sr = librosa.load(audio_path)

    # Define the parameters
    window_length_sec = 0.05  # 50 ms window length
    n_fft = 2048  # FFT size
    hop_length = int(sr * window_length_sec)  # Hop length based on window length
    window = "blackman"  # Window function

    # Calculate the STFT with the specified window length and hop length
    D = librosa.stft(
        y, n_fft=n_fft, hop_length=hop_length, win_length=n_fft, window=window
    )

    # Convert the amplitude spectrogram to magnitude
    D_mag = np.abs(D)

    # max_magnitude = np.max(D_mag)
    # min_magnitude = np.min(D_mag)
    # print(f"Maximum Magnitude: {max_magnitude}")
    # print(f"Minimum Magnitude: {min_magnitude}")

    # Find the indices of the top magnitude bins for each frame
    top_indices = np.argsort(D_mag, axis=0)[-40:]

    # Get corresponding frequencies for the top indices
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    top_frequencies = frequencies[top_indices]

    # Convert frequencies to MIDI notes for each frame
    midi_notes = librosa.hz_to_midi(top_frequencies)

    # Create a MIDIFile object
    midi = MIDIFile(1)

    # Add track name and tempo events
    track = 0
    time = 0
    midi.addTrackName(track, time, "Talking Piano")
    midi.addTempo(track, time, 60)

    # Add notes to the MIDI track based on magnitude threshold
    channel = 0
    velocity = 100  # Note velocity
    magnitude_threshold = 2  # Adjust this threshold as needed

    for i, notes in enumerate(midi_notes.T):
        for note in notes:
            if note != 0:  # Exclude notes with MIDI note number 0 (rest)
                # Convert MIDI note to frequency in Hz
                frequency = librosa.midi_to_hz(note)

                # Convert frequency to corresponding bin index
                frequency_bin = int(frequency * n_fft / sr)

                # Calculate the magnitude at the current time frame and frequency bin
                magnitude = D_mag[frequency_bin, i]

                # Check if magnitude is above the threshold
                if magnitude > magnitude_threshold:
                    # Convert time to seconds
                    start_time = i * hop_length / sr
                    duration = 0.05  # 50 milliseconds

                    # Calculate velocity
                    velocity = min(
                        round(127 * (np.log(magnitude + 1) / np.log(200 + 1))), 127
                    )

                    # Convert note to integer if it's not already
                    note_int = int(round(note))

                    # Add note to the MIDI track
                    midi.addNote(
                        track, channel, note_int, start_time, duration, velocity
                    )

    # Save the MIDI file
    output_file = "talking_piano.mid"
    with open(output_file, "wb") as file:
        midi.writeFile(file)

    print(f"MIDI file '{output_file}' created successfully!")
