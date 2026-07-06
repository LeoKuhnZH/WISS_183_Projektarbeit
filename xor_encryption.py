from functools import reduce
from log_unit import logger, Severity


class XOREncryption:
    @staticmethod
    def _make_binary_char(string: str) -> str:
        if len(string) >= 1:
            return f"{ord(string[0]):08b}"
        else:
            logger.log("Found an Empty Character", Severity.WARNING)
            return ""

    @staticmethod
    def _encrypt_single_xor(string: str, key: str) -> list[int]:
        if not string or not key:
            logger.log(message="String or key are empty", severity=Severity.ERROR)
            raise IndexError

        # Fold the key sequence over the char_bits using a nested XOR logic
        return reduce(
            lambda current_bits, next_key_bits: [
                c ^ k for c, k in zip(current_bits, next_key_bits)
            ],
            ([int(b) for b in XOREncryption._make_binary_char(k)] for k in key),
            [int(b) for b in XOREncryption._make_binary_char(string[0])]
        )

    @staticmethod
    def _encrypt_xor_encryption(string: str, key: str) -> list[list[int]]:
        logger.log("Beginning Encryption", Severity.INFO)
        return [XOREncryption._encrypt_single_xor(cha, key) for cha in string]

    @staticmethod
    def _to_binary_strings(nested_bits: list[list[int]]) -> list[str]:
        """
        Converts a list of bit-lists into a list of 8-character binary strings.
        Example: [[0, 1, ...], [1, 1, ...]] -> ["01...", "11..."]
        """
        logger.log("Turning the List of Lists of bits into a List of bytes", Severity.INFO)
        return ["".join(map(str, byte_list)) for byte_list in nested_bits]

    @staticmethod
    def to_full_string(nested_bits: list[list[int]]) -> str:
        """
        Directly converts the nested bits back into a human-readable string.
        Note: If you Xor every char with every key char, this will
        produce a string of length (len(string) * len(key)).
        """
        logger.log("Turning the List of Lists of Strings into a single String", Severity.INFO)
        binary_strings = XOREncryption._to_binary_strings(nested_bits)
        return "".join(chr(int(b, 2)) for b in binary_strings)

    @staticmethod
    def encrypter_xor(string: str, key: str) -> str:
        logger.log("Initializing Encryption", Severity.INFO)
        return XOREncryption.to_full_string(XOREncryption._encrypt_xor_encryption(string, key))
