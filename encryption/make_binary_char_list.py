from encryption.make_binary_char import make_binary_char


def make_binary_string(string: str) -> list[str]:
    return [make_binary_char(s) for s in string]