from encryption.make_binary_char import make_binary_char


def encrypt_single_xor(string: str, key: str) -> list[int]:
    if len(string) >= 1 and len(key) >= 1:
        return [int(bincha) ^ int(binkeypiece) for bincha, binkeypiece in zip(make_binary_char(string[0]), make_binary_char(key[0]))]
    else:
        raise IndexError