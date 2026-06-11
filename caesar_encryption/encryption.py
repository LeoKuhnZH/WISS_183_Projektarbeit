from caesar_encryption.encrypt_caesar_encryption import encrypt_caesar_encryption


class CaesarFlattener:
    @staticmethod
    def to_full_string(char_list: list[str]) -> str:
        return "".join(char_list)


def caesar_encrypt(string: str, shift: int) -> str:
    return CaesarFlattener.to_full_string(encrypt_caesar_encryption(string, shift))


def caesar_decrypt(string: str, shift: int) -> str:
    return caesar_encrypt(string, -shift)
