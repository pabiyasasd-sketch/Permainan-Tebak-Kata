"""
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# type "python speech.py" in terminal to run this code

duration = 5  # duration of recording in seconds
sample_rate = 44100  # sample rate in Hz

print("Speak now... (5 Seconds)")
recording = sd.rec(
  int(duration * sample_rate), # count of samples to record
  samplerate=sample_rate,      # sample rate
  channels=1,                  # 1 means recording in mono
  dtype="int16")               # data type for recording example
sd.wait()  # wait for recording to complete

wav.write("output.wav", sample_rate, recording)
print("Recording complete, starting speech recognition...")

recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio, language="id-ID")
    print(' ')
    print("You said:", text)
    print(' ')
    lang = input("What language do you want to translate to? (e.g., 'es' for Spanish, 'fr' for French): ").strip().lower()
    translator = Translator()
    translated = translator.translate(text, dest=lang)
    print(f"🌍 Translation to {lang}:", translated.text)
except sr.UnknownValueError:             # if google cannot understand the audio due to noise or silence
    print(' ')
    print("Speech not recognized :(")
except sr.RequestError as e:             # if there is no internet connection or the API is not available
    print(f"Service error: {e}")
"""
