# Raspberry Pi Zero W - USB HID Gadget Auto Setup

This guide automates the setup for making your Raspberry Pi Zero W act as a USB HID keyboard using `g_hid` and systemd service.

---

## ✅ STEP 1: Boot Config

### 1. Edit `/boot/firmware/config.txt`

```bash
sudo nano /boot/firmware/config.txt
```

**Add or ensure:**

```ini
[all]
dtoverlay=dwc2
```

**Comment this if exists:**

```ini
#dtoverlay=vc4-kms-v3d
```

---

### 2. Edit `/boot/firmware/cmdline.txt`

```bash
sudo nano /boot/firmware/cmdline.txt
```

Make sure it's a single line and includes this after `rootwait`:

```txt
modules-load=dwc2,g_hid
```

**Example:**

```txt
console=serial0,115200 console=tty1 root=PARTUUID=xxxx-xx rootfstype=ext4 fsck.repair=yes rootwait modules-load=dwc2,g_hid
```

---

## ✅ STEP 2: HID Setup Script

### 1. Create Script

```bash
sudo nano /usr/local/bin/hid_setup.sh
```

**Paste:**
```bash
#!/bin/bash

modprobe libcomposite
cd /sys/kernel/config/usb_gadget/
mkdir -p g1 && cd g1

echo 0x1d6b > idVendor
echo 0x0104 > idProduct
echo 0x0100 > bcdDevice
echo 0x0200 > bcdUSB

mkdir -p strings/0x409
echo "1234567890" > strings/0x409/serialnumber
echo "RaspberryPi" > strings/0x409/manufacturer
echo "Pi Zero HID" > strings/0x409/product

mkdir -p configs/c.1/strings/0x409
echo "HID Config" > configs/c.1/strings/0x409/configuration
echo 120 > configs/c.1/MaxPower

mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length

echo -ne '\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x05\x75\x01\x05\x08\x19\x01\x29\x05\x91\x02\x95\x01\x75\x03\x91\x01\x95\x06\x75\x08\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0' > functions/hid.usb0/report_desc

ln -s functions/hid.usb0 configs/c.1/
ls /sys/class/udc > UDC
```

### 2. Make it Executable

```bash
sudo chmod +x /usr/local/bin/hid_setup.sh
```

---

## ✅ STEP 3: systemd Service

```bash
sudo nano /etc/systemd/system/hidgadget.service
```

**Paste:**

```ini
[Unit]
Description=USB HID Gadget Setup
After=multi-user.target
Requires=systemd-modules-load.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/hid_setup.sh
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

### Enable Service

```bash
sudo systemctl daemon-reexec
sudo systemctl enable hidgadget.service
sudo systemctl start hidgadget.service
```

---

## ✅ STEP 4: Final Check

Reboot and check:

```bash
chmod +x setup_deckey_gadget.sh
sudo ./setup_deckey_gadget.sh
ls /dev/hidg0
```




```bash
sudo reboot
ls /dev/hidg0
```

**Make sure to use USB OTG port on the Pi!**
