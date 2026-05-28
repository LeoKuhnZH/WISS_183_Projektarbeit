from functools import reduce
from encryption.make_binary_char import make_binary_char

def encrypt_single_xor(string: str, key: str) -> list[int]:
    if not string or not key:
        raise IndexError

    # Convert the string char and all key chars into bit-lists first
    char_bits = [int(b) for b in make_binary_char(string[0])]
    key_bits_sequence = ([int(b) for b in make_binary_char(k)] for k in key)

    # Fold the key sequence over the char_bits using a nested XOR logic
    return reduce(
        lambda current_bits, next_key_bits: [
            c ^ k for c, k in zip(current_bits, next_key_bits)
        ],
        key_bits_sequence,
        char_bits
    )