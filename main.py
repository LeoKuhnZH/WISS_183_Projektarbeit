#!/usr/bin/env python3
import os
import sys

from xor_encryption.encryption import encrypter_xor

if __name__ == "__main__":
    # Check if the user provided enough arguments
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: ./file.py <data_or_file> <key_or_file> <filepath>")
        sys.exit(1)

    data_in = sys.argv[1]
    key_in = sys.argv[2]

    # Check if data_in is actually a path to an existing file
    if os.path.isfile(data_in):
        try:
            with open(data_in, "r", encoding="utf-8") as f:
                data_in = f.read()
        except Exception as e:
            print(f"Error reading file '{data_in}': {e}")
            sys.exit(1)

    # Check if key_in is actually a path to an existing file
    if os.path.isfile(key_in):
        try:
            with open(key_in, "r", encoding="utf-8") as f:
                key_in = f.read()
        except Exception as e:
            print(f"Error reading file '{key_in}': {e}")
            sys.exit(1)

    if len(sys.argv) == 3:
        print(encrypter_xor(string=data_in, key=key_in))

    elif len(sys.argv) == 4:
        output_path = sys.argv[3]

        with open(output_path, "wb") as binary_file:
            binary_file.write(
                encrypter_xor(string=data_in, key=key_in).encode("latin-1")
            )