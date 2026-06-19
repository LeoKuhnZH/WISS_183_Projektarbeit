from log_unit import Severity, logger


def make_binary_char(string: str) -> str:
    if len(string) >= 1:
        return f"{ord(string[0]):08b}"
    else:
        logger.log("Found an Empty Character", Severity.WARNING)
        return ""
