from encryption.encrypt_single import encrypt_single_xor


def encrypt_xor_encryption(string: str, key: str) -> list[list[int]]:
    return [encrypt_single_xor(cha, key) for cha in string]
