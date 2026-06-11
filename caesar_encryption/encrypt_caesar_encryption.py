from caesar_encryption.encrypt_single import encrypt_single_caesar

#text--> Verschiebung --> In Liste von verschlüsselten Zeichen
def encrypt_caesar_encryption(string: str, shift: int) -> list[str]:
    return [encrypt_single_caesar(cha, shift) for cha in string]
