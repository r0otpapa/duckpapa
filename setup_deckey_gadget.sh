#!/bin/bash
# Setup USB HID gadget for Deckpapa

echo "[*] Enabling HID USB gadget..."

modprobe libcomposite

cd /sys/kernel/config/usb_gadget || exit

# Create gadget
mkdir -p deckey
cd deckey

# USB IDs
echo 0x1d6b > idVendor      # Linux Foundation
echo 0x0104 > idProduct     # HID gadget
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB

# Strings
mkdir -p strings/0x409
echo "1234567890" > strings/0x409/serialnumber
echo "Deckey Inc." > strings/0x409/manufacturer
echo "Deckey USB Keyboard" > strings/0x409/product

# Configuration
mkdir -p configs/c.1
echo 250 > configs/c.1/MaxPower

# HID Function
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol     # Keyboard
echo 1 > functions/hid.usb0/subclass     # Boot Interface Subclass
echo 8 > functions/hid.usb0/report_length

# HID report descriptor for a standard keyboard
echo -ne \
  '\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01'\
  '\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x06\x75\x08'\
  '\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0' \
  > functions/hid.usb0/report_desc

# Bind function to config
ln -s functions/hid.usb0 configs/c.1/

# Activate gadget
echo "$(ls /sys/class/udc)" > UDC

echo "[✓] Deckey USB HID gadget ready."
