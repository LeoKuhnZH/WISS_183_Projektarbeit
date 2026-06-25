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
    'Z': '1100','Ä':'0101','Ö':'1110','Ü':'0011',
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

#Neuer Part audio Schlüssel
def create_frequencies(key):
    random.seed(key)

    freq0 = random.sample(range(300, 501), 3)
    freq1 = random.sample(range(600, 901), 3)

    return freq0, freq1

BIT_TIME = 0.8

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
    """Erzeugt Stille."""
    return np.zeros(int(SAMPLE_RATE * duration))

def code_to_audio(code, freq0, freq1, filename="output.wav"):
    """
    Wandelt 0/1-Code in eine WAV-Datei um.
    """

    audio = []

    for char in code:

        if char == "0":
            freq = random.choice(freq0)
            audio.extend(tone(freq, BIT_TIME))
            audio.extend(silence(0.02))

        elif char == "1":
            freq = random.choice(freq1)
            audio.extend(tone(freq, BIT_TIME))
            audio.extend(silence(0.02))

        elif char == " ":
            audio.extend(silence(0.30))

        elif char == "/":
            audio.extend(silence(0.80))

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

    #Option 4 Audio zu Code
def audio_to_code(filename, freq0, freq1):

    with wave.open(filename, "r") as wav:
        frames = wav.readframes(wav.getnframes())
        audio = np.frombuffer(frames, dtype=np.int16)

    audio = audio.astype(np.float32) / 32767

    def classify_tone(chunk):
        fft = np.fft.rfft(chunk)
        freqs = np.fft.rfftfreq(len(chunk), 1 / SAMPLE_RATE)
        peak_freq = freqs[np.argmax(np.abs(fft))]

        dist0 = min(abs(peak_freq - f) for f in freq0)
        dist1 = min(abs(peak_freq - f) for f in freq1)

        if abs(dist0 - dist1) < 20:
            return None
        return "0" if dist0 < dist1 else "1"

    block_size = int(SAMPLE_RATE * 0.02)   # 20ms Analysefenster
    block_duration = block_size / SAMPLE_RATE

    threshold = 0.04
    letter_gap = 0.20
    word_gap = 0.55

    bits = []
    current_bit = ""
    silence_duration = 0.0
    tone_chunks = []
    state = "silence"

    for i in range(0, len(audio), block_size):
        chunk = audio[i:i + block_size]
        if len(chunk) == 0:
            continue

        amplitude = np.max(np.abs(chunk))
        is_tone = amplitude >= threshold

        if is_tone:
            if state == "silence":
                if silence_duration >= word_gap:
                    if current_bit != "":
                        bits.append(current_bit)
                        current_bit = ""
                    bits.append("/")
                elif silence_duration >= letter_gap:
                    if current_bit != "":
                        bits.append(current_bit)
                        current_bit = ""
                silence_duration = 0.0
                tone_chunks = []
            tone_chunks.append(chunk)
            state = "tone"
            continue

        # silence
        if state == "tone" and tone_chunks:
            tone_chunk = np.concatenate(tone_chunks)
            bit = classify_tone(tone_chunk)
            if bit is not None:
                current_bit += bit
            tone_chunks = []

        silence_duration += block_duration
        state = "silence"

    if state == "tone" and tone_chunks:
        tone_chunk = np.concatenate(tone_chunks)
        bit = classify_tone(tone_chunk)
        if bit is not None:
            current_bit += bit

    if current_bit != "":
        bits.append(current_bit)

    return " ".join(bits)
#Main Programm
if __name__ == "__main__":
    print("0/1-Code Übersetzer")
    #Text -> Code
    print("1: Text -> Code")
    #Code -> Text
    print("2: Code -> Text")
    #Code -> audio
    print("3: Code -> Audio")
    #Audio -> Code -> Text
    print("4: Audio -> Text")

    choice = input("Option (1/2/3/4): ").strip()

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

     #Option 3 Text zu Audio
    elif choice == '3':

        text = input("Text eingeben: ")

        key = input("Schlüssel: ")

        try:

            code = encode(text)

            freq0, freq1 = create_frequencies(key)
            #Ausklammern Falls nötig für zwischen schritt

            print("Verwendete Frequenzen für 0:", freq0)

            print("Verwendete Frequenzen für 1:", freq1)

            code_to_audio(

                code,

                freq0,

                freq1

            )


        except ValueError as err:

            print("Fehler:", err)

    elif choice == '4':
        filename = input("WAV-Datei: ")
        key = input("Schlüssel: ")

        try:
            freq0, freq1 = create_frequencies(key)

            code = audio_to_code(filename, freq0, freq1)

            print("Raw Code:", code)

            text = decode(code)
            print("Text:", text)

        except Exception as err:
            print("Fehler:", err)


    else:
        print("Ungültige Auswahl.")