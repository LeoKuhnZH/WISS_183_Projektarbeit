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


if __name__ == "__main__":
    print("0/1-Code Übersetzer")
    print("1: Text -> Code")
    print("2: Code -> Text")

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

    else:
        print("Ungültige Auswahl.")