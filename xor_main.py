#!/usr/bin/env python3
import os
import sys

from xor_encryption.encryption import encrypter_xor

def _find_string(input_string: str) -> str:
    if os.path.isfile(input_string):
        try:
            with open(input_string, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file '{input_string}': {e}")
            sys.exit(1)

    else:
        return input_string

if __name__ == "__main__":
    # Check if the user provided enough arguments
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: ./file.py <data_or_file> <key_or_file> <filepath>")
        sys.exit(1)

    data_in = sys.argv[1]
    key_in = sys.argv[2]

    # Check if data_in is actually a path to an existing file
    data_in = _find_string(data_in)

    # Check if key_in is actually a path to an existing file
    key_in = _find_string(key_in)

    if len(sys.argv) == 3:
        print(encrypter_xor(string=data_in, key=key_in))

    elif len(sys.argv) == 4:
        output_path = sys.argv[3]

        with open(output_path, "wb") as binary_file:
            binary_file.write(
                encrypter_xor(string=data_in, key=key_in).encode("latin-1")
            )
