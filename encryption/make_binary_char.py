def make_binary_char(string: str) -> str:
    if len(string) >= 1:
        return f"{ord(string[0]):08b}"
    else:
        return ""
