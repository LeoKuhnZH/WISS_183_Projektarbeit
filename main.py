#!/usr/bin/env python3
import os
import sys

from caesar_encryption.encryption import caesar_decrypt, caesar_encrypt
from xor_encryption.encryption import encrypter_xor


def read_text_or_file(value: str) -> str:
    if not os.path.isfile(value):
        return value

    try:
        with open(value, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file '{value}': {e}")
        sys.exit(1)


def print_usage() -> None:
    print("Usage:")
    print("  ./file.py xor <data_or_file> <key_or_file> [output_file]")
    print("  ./file.py caesar-encrypt <data_or_file> <shift> [output_file]")
    print("  ./file.py caesar-decrypt <data_or_file> <shift> [output_file]")


def write_or_print(result: str, output_path: str | None = None) -> None:
    if output_path is None:
        print(result)
        return

    with open(output_path, "wb") as binary_file:
        binary_file.write(result.encode("latin-1"))


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print_usage()
        sys.exit(1)

    mode = sys.argv[1]
    data_in = read_text_or_file(sys.argv[2])
    key_or_shift = sys.argv[3]
    output_path = sys.argv[4] if len(sys.argv) == 5 else None

    if mode == "xor":
        key_in = read_text_or_file(key_or_shift)
        write_or_print(encrypter_xor(string=data_in, key=key_in), output_path)
    elif mode in ["caesar-encrypt", "caesar-decrypt"]:
        try:
            shift = int(key_or_shift)
        except ValueError:
            print("Shift must be a number.")
            sys.exit(1)

        if mode == "caesar-encrypt":
            write_or_print(caesar_encrypt(string=data_in, shift=shift), output_path)
        else:
            write_or_print(caesar_decrypt(string=data_in, shift=shift), output_path)
    else:
        print_usage()
        sys.exit(1)
