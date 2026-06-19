from functools import reduce

from log_unit import logger, Severity
from xor_encryption.make_binary_char import make_binary_char


def encrypt_single_xor(string: str, key: str) -> list[int]:
    if not string or not key:
        logger.log(message="String or key are empty", severity=Severity.ERROR)
        raise IndexError

    # Fold the key sequence over the char_bits using a nested XOR logic
    return reduce(
        lambda current_bits, next_key_bits: [
            c ^ k for c, k in zip(current_bits, next_key_bits)
        ],
        ([int(b) for b in make_binary_char(k)] for k in key),
        [int(b) for b in make_binary_char(string[0])]
    )
