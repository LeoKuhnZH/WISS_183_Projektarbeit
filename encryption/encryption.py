from encryption.encrypt_single import encrypt_single_xor
from encryption.make_binary_char import make_binary_char

def _encrypt_xor_encryption(string: str, key: str) -> list[list[int]]:
    return [encrypt_single_xor(cha, keypiece) for cha in string for keypiece in key]

class XORFlattener:
    @staticmethod
    def _to_binary_strings(nested_bits: list[list[int]]) -> list[str]:
        """
        Converts a list of bit-lists into a list of 8-character binary strings.
        Example: [[0, 1, ...], [1, 1, ...]] -> ["01...", "11..."]
        """
        return ["".join(map(str, byte_list)) for byte_list in nested_bits]

    @staticmethod
    def to_full_string(nested_bits: list[list[int]]) -> str:
        """
        Directly converts the nested bits back into a human-readable string.
        Note: If you XOR'd every char with every key char, this will
        produce a string of length (len(string) * len(key)).
        """
        binary_strings = XORFlattener._to_binary_strings(nested_bits)
        return "".join(chr(int(b, 2)) for b in binary_strings)

def encryption(string: str, key: str) -> str:
    return XORFlattener.to_full_string(_encrypt_xor_encryption(string, key))