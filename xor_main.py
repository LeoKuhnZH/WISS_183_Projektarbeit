#!/usr/bin/env python3
import os
import sys

from log_unit import logger
from log_unit import Severity

from xor_encryption.encryption import encrypter_xor

def _find_string(input_string: str) -> str:
    logger.log(message="Initiated Program", severity=Severity.INFO)
    if os.path.isfile(input_string):
        try:
            with open(input_string, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.log(message=e, severity=Severity.ERROR)
            sys.exit(1)

    else:
        return input_string

if __name__ == "__main__":
    try:
        # Check if the user provided enough arguments
        if len(sys.argv) != 3 and len(sys.argv) != 4:
            logger.log(message="Incorrect number of arguments", severity=Severity.ERROR)
            print("Usage: ./file.py <data_or_file> <key_or_file> <filepath>")
            raise TypeError

        data_in = sys.argv[1]
        key_in = sys.argv[2]

        # Check if data_in is actually a path to an existing file
        data_in = _find_string(data_in)

        # Check if key_in is actually a path to an existing file
        key_in = _find_string(key_in)

        if len(sys.argv) == 3:
            logger.log(message="Starting program without output file", severity=Severity.INFO)
            print(encrypter_xor(string=data_in, key=key_in))
            logger.log(message="Program Execution finished", severity=Severity.INFO)
            logger.save_to_file()
            logger.clear()

        elif len(sys.argv) == 4:
            logger.log(message="Starting program with output file", severity=Severity.INFO)
            output_path = sys.argv[3]

            with open(output_path, "wb") as binary_file:
                logger.log(message="writing to file", severity=Severity.INFO)
                binary_file.write(
                    encrypter_xor(string=data_in, key=key_in).encode("latin-1")
                )
                logger.log(message="Program Execution finished", severity=Severity.INFO)
                logger.save_to_file()
                logger.clear()
    except Exception as e:
        logger.log(message="Program Failed", severity=Severity.CRITICAL)
        logger.save_to_file()
        print(logger)
        logger.clear()
        sys.exit(1)
