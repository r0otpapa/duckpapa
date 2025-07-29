import time

# HID report: [Modifier, Reserved, Key1, Key2, Key3, Key4, Key5, Key6]
# Example: Left Shift (0x02) + 'H' (0x0B) = 'H'
def write_key(report):
    with open("/dev/hidg0", "wb") as fd:
        fd.write(report)
        fd.write(b'\x00' * 8)  # release keys

def type_string(string):
    char_map = {
        'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07,
        'e': 0x08, 'f': 0x09, 'g': 0x0A, 'h': 0x0B,
        'i': 0x0C, 'j': 0x0D, 'k': 0x0E, 'l': 0x0F,
        'm': 0x10, 'n': 0x11, 'o': 0x12, 'p': 0x13,
        'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17,
        'u': 0x18, 'v': 0x19, 'w': 0x1A, 'x': 0x1B,
        'y': 0x1C, 'z': 0x1D,
        ' ': 0x2C,
        '\n': 0x28
    }

    for char in string:
        keycode = char_map.get(char.lower())
        if keycode:
            write_key(bytes([0x00, 0x00, keycode, 0x00, 0x00, 0x00, 0x00, 0x00]))
            time.sleep(0.1)

type_string("hello from pi \n r0otpapa")
