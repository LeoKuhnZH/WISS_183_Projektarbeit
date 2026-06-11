def encrypt_single_caesar(char: str, shift: int) -> str:
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


#Encrypting 
def caesar_encrypt(string: str, shift: int) -> str:
    return "".join(encrypt_single_caesar(c, shift) for c in string)


#Decrypting 
def caesar_decrypt(string: str, shift: int) -> str:
    return caesar_encrypt(string, -shift)