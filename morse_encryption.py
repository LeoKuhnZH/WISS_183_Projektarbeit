import random
import wave

import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

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
class MorseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Morse Encryption Prototype")
        self.root.geometry("700x450")

        tk.Label(root, text="Eingabe (Text oder Code)", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.input_field = tk.Text(root, height=8)
        self.input_field.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Label(root, text="Schlüssel für Audio", anchor="w").pack(fill="x", padx=10)
        self.key_field = tk.Entry(root)
        self.key_field.pack(fill="x", padx=10, pady=5)

        button_frame = tk.Frame(root)
        button_frame.pack(fill="x", padx=10, pady=8)

        tk.Button(button_frame, text="Text -> Code", command=self.encode_text).pack(side="left", padx=5)
        tk.Button(button_frame, text="Code -> Text", command=self.decode_text).pack(side="left", padx=5)
        tk.Button(button_frame, text="Text -> Audio", command=self.text_to_audio).pack(side="left", padx=5)
        tk.Button(button_frame, text="WAV hochladen", command=self.upload_audio).pack(side="left", padx=5)

        tk.Label(root, text="Ergebnis", anchor="w").pack(fill="x", padx=10, pady=(10, 0))
        self.output_field = tk.Text(root, height=8)
        self.output_field.pack(fill="both", expand=True, padx=10, pady=5)

    def _get_input_text(self):
        return self.input_field.get("1.0", "end").strip()

    def _set_output(self, text):
        self.output_field.delete("1.0", "end")
        self.output_field.insert("1.0", text)

    def encode_text(self):
        text = self._get_input_text()
        if not text:
            messagebox.showwarning("Eingabe fehlt", "Bitte gib einen Text ein.")
            return

        try:
            self._set_output(encode(text))
        except ValueError as err:
            messagebox.showerror("Fehler", str(err))

    def decode_text(self):
        code = self._get_input_text()
        if not code:
            messagebox.showwarning("Eingabe fehlt", "Bitte gib einen Morse-Code ein.")
            return

        try:
            self._set_output(decode(code))
        except ValueError as err:
            messagebox.showerror("Fehler", str(err))

    def text_to_audio(self):
        text = self._get_input_text()
        key = self.key_field.get().strip()
        if not text:
            messagebox.showwarning("Eingabe fehlt", "Bitte gib einen Text ein.")
            return
        if not key:
            messagebox.showwarning("Schlüssel fehlt", "Bitte gib einen Schlüssel ein.")
            return

        try:
            code = encode(text)
            freq0, freq1 = create_frequencies(key)
            filename = filedialog.asksaveasfilename(
                defaultextension=".wav",
                initialfile="output.wav",
                filetypes=[("WAV-Dateien", "*.wav")],
            )
            if not filename:
                return

            code_to_audio(code, freq0, freq1, filename)
            self._set_output(f"Code: {code}\n\nAudio gespeichert unter:\n{filename}")
            messagebox.showinfo("Erfolg", f"Audio gespeichert unter:\n{filename}")
        except ValueError as err:
            messagebox.showerror("Fehler", str(err))
        except Exception as err:
            messagebox.showerror("Fehler", str(err))

    def upload_audio(self):
        key = self.key_field.get().strip()
        if not key:
            messagebox.showwarning("Schlüssel fehlt", "Bitte gib einen Schlüssel ein.")
            return

        filename = filedialog.askopenfilename(filetypes=[("WAV-Dateien", "*.wav")])
        if not filename:
            return

        try:
            freq0, freq1 = create_frequencies(key)
            code = audio_to_code(filename, freq0, freq1)
            text = decode(code)
            self._set_output(f"Code: {code}\n\nText: {text}")
        except Exception as err:
            messagebox.showerror("Fehler", str(err))


if __name__ == "__main__":
    root = tk.Tk()
    MorseGUI(root)
    root.mainloop()