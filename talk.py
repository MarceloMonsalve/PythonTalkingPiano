import os
import wave
import time
import threading
import tkinter as tk
import pyaudio
from pydub import AudioSegment
import pygame
import stft


class VoiceRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        pygame.init()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        self.record_button = tk.Button(
            self.button_frame,
            text="⏺️",
            font=("Arial", 120, "bold"),
            bg="black",
            command=self.start_recording,
        )
        self.record_button.pack(side=tk.LEFT, padx=10)

        self.play_button = tk.Button(
            self.button_frame,
            text="⏯️",
            font=("Arial", 120, "bold"),
            bg="black",
            command=self.start_playing,
        )
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.label = tk.Label(text="00:00:00", font=("Andale Mono", 24))
        self.label.pack()
        self.recording = False
        self.playing = False
        if os.path.exists("recording.wav"):
            os.remove("recording.wav")
        self.root.mainloop()

    def start_recording(self):
        if self.recording:
            self.recording = False
            self.record_button.config(bg="white")
        else:
            self.recording = True
            self.record_button.config(bg="red")
            threading.Thread(target=self.record).start()

    def start_playing(self):
        if self.playing:
            self.playing = False
            self.play_button.config(bg="green")
        else:
            self.playing = True
            self.play_button.config(bg="red")
            threading.Thread(target=self.play).start()

    def play(self):
        if not self.recording:
            pygame.mixer.music.load("talking_piano.mid")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            self.playing = False

    def record(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
        )
        frames = []
        start = round(time.time() * 100)
        while self.recording:
            data = stream.read(1024)
            frames.append(data)
            passed = round(time.time() * 100) - start
            subsecs = passed % 100
            secs = (passed // 100) % 60
            mins = (passed // 100) // 60
            self.label.config(
                text=f"{int(mins):02d}:{int(secs):02d}.{int(subsecs):02d}"
            )
        stream.stop_stream()
        stream.close()
        audio.terminate()

        sound_file = wave.open("recording.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()
        audio = AudioSegment.from_file("recording.wav")
        normalized_audio = audio.normalize()
        normalized_audio.export("recording.wav", format="wav")
        self.label.config(text="00:00:00")
        stft.create_midi()


VoiceRecorder()
