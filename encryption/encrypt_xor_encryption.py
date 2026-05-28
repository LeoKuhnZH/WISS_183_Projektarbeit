from encryption.encrypt_single import encrypt_single_xor


def encrypt_xor_encryption(string: str, key: str) -> list[list[int]]:
    return [encrypt_single_xor(cha, keypiece) for cha in string for keypiece in key]