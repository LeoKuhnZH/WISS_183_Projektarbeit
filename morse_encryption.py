import wave

import numpy as np
import random

#Encrypt Festlegen

encrypt ={
'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0',
    'F': '0010', 'G': '110', 'H': '0000', 'I': '00', 'J': '0111',
    'K': '101', 'L': '0100', 'M': '11', 'N': '10', 'O': '111',
    'P': '0110', 'Q': '1101', 'R': '010', 'S': '000', 'T': '1',
    'U': '001', 'V': '0001', 'W': '011', 'X': '1001', 'Y': '1011',
    'Z': '1100',
    '0': '11111', '1': '01111', '2': '00111', '3': '00011',
    '4': '00001', '5': '00000', '6': '10000', '7': '11000',
    '8': '11100', '9': '11110',
    '.': '010101', ',': '110011', '?': '001100', "'": '011110',
    '!': '101011', '/': '10010', '(': '10110', ')': '101101',
    '&': '01000', ':': '111000', ';': '101010', '=': '10001',
    '+': '01010', '-': '100001', '_': '001101', '"': '010010',
    '$': '0001001', '@': '011010', ' ': '/'  # Space as '/'
}
# Funktion
decrypt = {v: k for k, v in encrypt.items()}

#Audio Part 1
SAMPLE_RATE = 44100

FREQ_0 = [440, 523, 659]
FREQ_1 = [392, 587, 784]

BIT_TIME = 1.5

#Encod Decod


def encode(text):
    #Wandelt Text in 0/1-Code um.
    try:
        return ' '.join(encrypt[char] for char in text.upper())
    except KeyError as e:
        raise ValueError(f"Zeichen '{e.args[0]}' wird nicht unterstützt.")


def decode(code):
    #Wandelt 0/1-Code in Text um."""
    try:
        return ''.join(decrypt[symbol] for symbol in code.split(' '))
    except KeyError as e:
        raise ValueError(f"Code '{e.args[0]}' ist ungültig.")

#Funktion Audio

def tone(freq, duration):
    """
    Erzeugt einen Sinuston.
    """
    t = np.linspace(
        0,
        duration,
        int(SAMPLE_RATE * duration),
        False
    )

    return np.sin(2 * np.pi * freq * t)

def silence(duration):
    return np.zeros(int(SAMPLE_RATE * duration))
    """
    Erzeugt Stille.
    """
    return np.zeros(
        int(SAMPLE_RATE * duration)
    )

def code_to_audio(code, filename="output.wav"):
    """
    Wandelt 0/1-Code in eine WAV-Datei um.
    """

    audio = []

    for char in code:

        if char == "0":
            freq = random.choice(FREQ_0)
            audio.extend(tone(freq, BIT_TIME))
            audio.extend(silence(0.02))

        elif char == "1":
            freq = random.choice(FREQ_1)
            audio.extend(tone(freq, BIT_TIME))
            audio.extend(silence(0.02))

        elif char == " ":
            audio.extend(silence(0.08))

        elif char == "/":
            audio.extend(silence(0.15))

    audio = np.array(audio)

    # Für WAV-Datei skalieren
    audio = (
        audio * 32767
    ).astype(np.int16)

    with wave.open(filename, "w") as wav:

        wav.setnchannels(1)      # Mono
        wav.setsampwidth(2)      # 16 Bit
        wav.setframerate(SAMPLE_RATE)

        wav.writeframes(
            audio.tobytes()
        )

    print(f"WAV gespeichert als: {filename}")



if __name__ == "__main__":
    print("0/1-Code Übersetzer")
    print("1: Text -> Code")
    print("2: Code -> Text")
    #Versuch audio
    print("3: Code -> Audio")

    choice = input("Option (1/2): ").strip()

    if choice == '1':
        text = input("Text eingeben: ")
        try:
            print("Code:", encode(text))
        except ValueError as err:
            print("Fehler:", err)

    elif choice == '2':
        code = input("Code eingeben (Leerzeichen zwischen Zeichen, '/' für Leerzeichen): ")
        try:
            print("Text:", decode(code))
        except ValueError as err:
            print("Fehler:", err)

    elif choice == '3':

        text = input("Text eingeben:")

        try:
            code = encode(text)
            print("Code:", code)

            code_to_audio(code)
        except ValueError as err:
            print("Fehler:", err)


    else:
        print("Ungültige Auswahl.")