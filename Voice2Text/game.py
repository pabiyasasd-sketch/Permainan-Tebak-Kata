import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import time
import random

words_by_level = {
    "easy": ["cat", "dog", "fish", "bird", "tree", "house", "car", "book", "chair", "table"],
    "medium": ["elephant", "giraffe", "dolphin", "kangaroo", "penguin", "tiger", "zebra", "monkey", "panda", "koala"],
    "hard": ["hippopotamus", "rhinoceros", "chimpanzee", "orangutan", "platypus", "armadillo", "porcupine", "salamander", "crocodile", "alligator"],
    "impossible(bonus)": ["antidisestablishmentarianism", "floccinaucinihilipilification", "pneumonoultramicroscopicsilicovolcanoconiosis", "supercalifragilisticexpialidocious", "hippopotomonstrosesquipedaliophobia"]
}

poin = 0

# Fungsi penghitung mundur
def countdown_timer(total_seconds):
    while total_seconds > 0:
        minutes, seconds = divmod(total_seconds, 60)
        print(f"\rWaktu Sisa: {minutes:02d}:{seconds:02d}", end="")
        time.sleep(1)
        total_seconds -= 1
    print("\rWaktunya!        ")

# Fungsi permainan
def game():
    global poin
    # Level progresi standar yang wajib dilewati
    levels = ["easy", "medium", "hard"]
    
    # LOOP LUAR: Mengulang level-level standar
    for level in levels:
        print(' ')
        print(f"Level Mulai: {level.upper()}")
        print(' ')
        time.sleep(1.5)
        
        # LOOP DALAM: Mengulang tepat 3 kali untuk level saat ini
        for i in range(1, 4):
            duration = 10  # durasi perekaman dalam detik
            sample_rate = 44100  # laju sampel dalam Hz

            print(f"\n[Level: {level.capitalize()}] Kata {i} of 3")
            time.sleep(1)
            
            # Pilih kata acak dari level yang aktif
            current_word = random.choice(words_by_level[level])
            print(f"Kata Target: {current_word}")
            print(' ')
            print("Bilang Sekarang!")
            
            # Mulai perekaman dan hitung mundur secara bersamaan
            recording = sd.rec(
                int(duration * sample_rate),
                samplerate=sample_rate,
                channels=1,
                dtype="int16"
            )
            countdown_timer(10)
            sd.wait()  # tunggu sampai perekaman selesai

            wav.write("output.wav", sample_rate, recording)
            print("Recording complete! Starting speech recognition...")

            recognizer = sr.Recognizer()
            with sr.AudioFile("output.wav") as source:
                audio = recognizer.record(source)

            try:
                # Mengenali input suara berbahasa Indonesia
                text = recognizer.recognize_google(audio, language="id-ID")
                print(' ')
                print("Kamu bilang:", text)
                print(' ')
                time.sleep(1)
                
                # Terjemahkan ke bahasa Inggris untuk membandingkan dengan kata target
                translator = Translator()
                translated = translator.translate(text, dest="en")
                print("🌍 English Translation:", translated.text)
                
                if translated.text.lower() == current_word.lower():
                    print("✅ Benar!")
                    poin += 5
                else:
                    print("❌ Salah! Kata yang benar adalah:", current_word)
                    poin -= 2
                
                print(f"Current Points: {poin}")

            except sr.UnknownValueError:
                print(' ')
                print("❌ Kata tidak dikenali :(")
                time.sleep(0.5)
                print("Ke round selanjutnya...")
                time.sleep(1)
                
            except sr.RequestError as e:
                print(f"Service error: {e}")
                time.sleep(1)
                
    # round bonus
    print(' ')
    print("- Kamu sudah MENANG Gamenya! -")
    print(f"Total poin: {poin} poin")
    print(' ')

    time.sleep(1)
    # apakah pemain ingin mencoba bonus round
    bonus_choice = input("Apakah Anda ingin mencoba Bonus Round yang sangat sulit untuk kesempatan mendapatkan p- DOLLAR! DOLLAR SAJA! (y/n): ")
    
    if bonus_choice.lower() == "y":
        level = "impossible(bonus)"
        print(" ")
        print(f": BONUS ROUND :")
        print(" ")
        time.sleep(1.5)
        
        for i in range(1, 4):
            duration = 10
            sample_rate = 44100

            print(f"\n[Level: Bonus] Kata {i} of 3")
            time.sleep(1)
            
            current_word = random.choice(words_by_level[level])
            print(f"Kata Target: {current_word}")
            print(' ')
            print("Bilang Sekarang!")
            
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
            countdown_timer(10)
            sd.wait()

            wav.write("output.wav", sample_rate, recording)
            print("Recording complete! Starting speech recognition...")

            recognizer = sr.Recognizer()
            with sr.AudioFile("output.wav") as source:
                audio = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio, language="id-ID")
                print(' ')
                print("Kamu bilang:", text)
                print(' ')
                time.sleep(1)
                
                translator = Translator()
                translated = translator.translate(text, dest="en")
                print("🌍 Terjemahan Inggris:", translated.text)
                
                # Jika benar saat bonus round, berikan 15 poin
                if translated.text.lower() == current_word.lower():
                    print("✅ Benar Sekali! Kamu mendapatkan 15 poin tambahan!")
                    poin += 15
                else:
                    print("❌ Tet-toot! Kata yang benar adalah:", current_word)
                    poin -= 2
                
                print(f"Current Points: {poin}")

            except sr.UnknownValueError:
                print(' ')
                print("❌ Kata tidak dikenali :(")
                time.sleep(0.5)
                print("Ke kata berikutnya...")
                time.sleep(1)
            except sr.RequestError as e:
                print(f"Service error: {e}")
                time.sleep(1)
    else:
        print("\nAnda memilih untuk melewati Bonus Round. Pilihan yang bijak!")

    # Akhir permainan
    print(' ')
    print(": Yay!!! Bonus roundnya SELESAI! :")
    print(f"Total p- DOLLAR: {poin} DOLLAR")
    print(' ')

# Inisialisasi menu
print("Selamat datang di permainan tebak kata!")
time.sleep(1)
print("Permainan ini akan menguji kemampuan Anda dalam mengenali kata-kata bahasa inggris yang diucapkan.")
time.sleep(1)

ready = input("Apakah Anda siap untuk bermain? (y/n): ")
if ready.lower() == "y":
    print("\nGame starting...")
    time.sleep(1)
    game()
else:
    print("Baiklah, sampai jumpa lain kali!")
    exit()
