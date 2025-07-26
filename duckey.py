# -*- coding: utf-8 -*-
import time
import sys
import os

HID_DEVICE = "/dev/hidg0"

# Modifier constants
MOD_NONE = 0x00
MOD_LCTRL = 0x01
MOD_LSHIFT = 0x02
MOD_LALT = 0x04
MOD_LGUI = 0x08

# ASCII to HID Key Map
KEYMAP = {
    'a': (MOD_NONE, 0x04), 'b': (MOD_NONE, 0x05), 'c': (MOD_NONE, 0x06), 'd': (MOD_NONE, 0x07),
    'e': (MOD_NONE, 0x08), 'f': (MOD_NONE, 0x09), 'g': (MOD_NONE, 0x0A), 'h': (MOD_NONE, 0x0B),
    'i': (MOD_NONE, 0x0C), 'j': (MOD_NONE, 0x0D), 'k': (MOD_NONE, 0x0E), 'l': (MOD_NONE, 0x0F),
    'm': (MOD_NONE, 0x10), 'n': (MOD_NONE, 0x11), 'o': (MOD_NONE, 0x12), 'p': (MOD_NONE, 0x13),
    'q': (MOD_NONE, 0x14), 'r': (MOD_NONE, 0x15), 's': (MOD_NONE, 0x16), 't': (MOD_NONE, 0x17),
    'u': (MOD_NONE, 0x18), 'v': (MOD_NONE, 0x19), 'w': (MOD_NONE, 0x1A), 'x': (MOD_NONE, 0x1B),
    'y': (MOD_NONE, 0x1C), 'z': (MOD_NONE, 0x1D),

    '1': (MOD_NONE, 0x1E), '2': (MOD_NONE, 0x1F), '3': (MOD_NONE, 0x20), '4': (MOD_NONE, 0x21),
    '5': (MOD_NONE, 0x22), '6': (MOD_NONE, 0x23), '7': (MOD_NONE, 0x24), '8': (MOD_NONE, 0x25),
    '9': (MOD_NONE, 0x26), '0': (MOD_NONE, 0x27),

    ' ': (MOD_NONE, 0x2C), '\n': (MOD_NONE, 0x28), '\t': (MOD_NONE, 0x2B),
    '-': (MOD_NONE, 0x2D), '=': (MOD_NONE, 0x2E), '[': (MOD_NONE, 0x2F), ']': (MOD_NONE, 0x30),
    '\\': (MOD_NONE, 0x31), ';': (MOD_NONE, 0x33), "'": (MOD_NONE, 0x34), '`': (MOD_NONE, 0x35),
    ',': (MOD_NONE, 0x36), '.': (MOD_NONE, 0x37), '/': (MOD_NONE, 0x38),

    '!': (MOD_LSHIFT, 0x1E), '@': (MOD_LSHIFT, 0x1F), '#': (MOD_LSHIFT, 0x20),
    '$': (MOD_LSHIFT, 0x21), '%': (MOD_LSHIFT, 0x22), '^': (MOD_LSHIFT, 0x23),
    '&': (MOD_LSHIFT, 0x24), '*': (MOD_LSHIFT, 0x25), '(': (MOD_LSHIFT, 0x26),
    ')': (MOD_LSHIFT, 0x27), '_': (MOD_LSHIFT, 0x2D), '+': (MOD_LSHIFT, 0x2E),
    '{': (MOD_LSHIFT, 0x2F), '}': (MOD_LSHIFT, 0x30), '|': (MOD_LSHIFT, 0x31),
    ':': (MOD_LSHIFT, 0x33), '"': (MOD_LSHIFT, 0x34), '~': (MOD_LSHIFT, 0x35),
    '<': (MOD_LSHIFT, 0x36), '>': (MOD_LSHIFT, 0x37), '?': (MOD_LSHIFT, 0x38)
}


def send_key(mod, key):
    with open(HID_DEVICE, 'rb+') as fd:
        fd.write(bytes([mod, 0x00, key, 0x00, 0x00, 0x00, 0x00, 0x00]))
        time.sleep(0.05)
        fd.write(b'\x00' * 8)
        time.sleep(0.05)


def send_string(text):
    for char in text:
        if char.lower() in KEYMAP:
            mod, key = KEYMAP[char.lower()]
            if char.isupper():
                mod |= MOD_LSHIFT
            send_key(mod, key)
        elif char == '\n':
            send_key(MOD_NONE, 0x28)
        elif char == '\t':
            send_key(MOD_NONE, 0x2B)
        else:
            print(f"[!] Unsupported char: {char}")
        time.sleep(0.01)


def run_script(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue

            parts = line.split()
            cmd = parts[0].upper()

            if cmd == "STRING":
                send_string(" ".join(parts[1:]))
            elif cmd == "ENTER":
                send_key(MOD_NONE, 0x28)
            elif cmd == "TAB":
                send_key(MOD_NONE, 0x2B)
            elif cmd == "CTRL":
                send_key(MOD_LCTRL, KEYMAP[parts[1].lower()][1])
            elif cmd == "ALT":
                send_key(MOD_LALT, KEYMAP[parts[1].lower()][1])
            elif cmd == "GUI":
                send_key(MOD_LGUI, KEYMAP[parts[1].lower()][1])
            elif cmd == "DELAY":
                time.sleep(int(parts[1]) / 1000)
            else:
                print(f"[!] Unknown command: {cmd}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: sudo python3 duckey.py notepad.txt")
        sys.exit(1)

    run_script(sys.argv[1])
