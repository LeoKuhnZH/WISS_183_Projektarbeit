from log_unit import logger, Severity
from xor_encryption.encrypt_single import encrypt_single_xor


def encrypt_xor_encryption(string: str, key: str) -> list[list[int]]:
    logger.log("Beginning Encryption", Severity.INFO)
    return [encrypt_single_xor(cha, key) for cha in string]
