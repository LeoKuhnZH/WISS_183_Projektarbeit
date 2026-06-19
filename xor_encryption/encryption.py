from log_unit import logger, Severity
from xor_encryption.encrypt_xor_encryption import encrypt_xor_encryption


class XORFlattener:
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
        binary_strings = XORFlattener._to_binary_strings(nested_bits)
        return "".join(chr(int(b, 2)) for b in binary_strings)


def encrypter_xor(string: str, key: str) -> str:
    logger.log("Initializing Encryption", Severity.INFO)
    return XORFlattener.to_full_string(encrypt_xor_encryption(string, key))
