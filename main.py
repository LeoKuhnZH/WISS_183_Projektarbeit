#!/usr/bin/env python3
import sys

from encryption.encryption import encrypter_xor

if __name__ == "__main__":
    # Check if the user provided enough arguments
    if len(sys.argv) == 3 or len(sys.argv) == 4:
        print("Usage: ./file.py <data> <key>")
        sys.exit(1)

    data_in = sys.argv[1]
    key_in = sys.argv[2]

    if len(sys.argv) == 3:

        print(encrypter_xor(string=data_in, key=key_in))

    elif len(sys.argv) == 4:

        output_path = sys.argv[3]

        with open(output_path, "wb") as binary_file:
            binary_file.write(encrypter_xor(string=data_in, key=key_in).encode('latin-1'))
