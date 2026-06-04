import winsound
import time
FREQ_0 = 500    # Hz
FREQ_1 = 1000   # Hz
BIT_TIME = 100  # ms
def play_binary(binary_code):
    for char in binary_code:
        if char == '0':
            winsound.Beep(FREQ_0, BIT_TIME)

        elif char == '1':
            winsound.Beep(FREQ_1, BIT_TIME)

        elif char == ' ':
            time.sleep(0.3)

        elif char == '/':
            time.sleep(0.7)

code = "0000 01 0100"
play_binary(code)