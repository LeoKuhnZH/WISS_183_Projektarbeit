
def encrypt_single_caesar(char: str, shift: int) -> str:
    if not char:
        raise IndexError

    if "A" <= char <= "Z":
        base = ord("A")
    elif "a" <= char <= "z":
        base = ord("a")
    else:
        return char

    return chr((ord(char) - base + shift) % 26 + base)
