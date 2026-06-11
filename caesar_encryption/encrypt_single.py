
def encrypt_single_caesar(char: str, shift: int) -> str:
    #leer = Error
    if not char:
        raise IndexError

    if "A" <= char <= "Z":
        base = ord("A")
    elif "a" <= char <= "z":
        base = ord("a")
    else:
        return char
    #Gross- und Kleinbuchstaben werden getrennt.

    
    return chr((ord(char) - base + shift) % 26 + base)


