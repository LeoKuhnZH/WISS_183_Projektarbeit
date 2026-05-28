#!/usr/bin/env python3
from encryption.encryption import encrypter_xor
import sys


if __name__ == "__main__":
    # Check if the user provided enough arguments
    if len(sys.argv) != 3:
        print("Usage: ./file.py <data> <key>")
        sys.exit(1)

    data_in = sys.argv[1]
    key_in = sys.argv[2]

    print(encrypter_xor(string=data_in, key=key_in))