# 🐥 Raspberry Pi Ducky Plug & Play - Auto Boot Setup Guide

This guide explains how to automatically run a Ducky script at boot using a `.sh` script and a systemd service on Raspberry Pi or Linux.

---

## 📁 Folder Structure

```
/home/kali/ducky/
├── duckey.py
├── plug_duck.sh
├── payloads/
│   └── notepad2.txt
```

---

## ✅ Step 1: `plug_duck.sh` Script

**Create the shell script:**

```bash
sudo nano /home/kali/ducky/plug_duck.sh
```

**Paste this:**

```bash
#!/bin/bash
sleep 5
python3 /home/kali/ducky/duckey.py '/home/kali/ducky/payloads/notepad2.txt'
```

**Make it executable:**

```bash
chmod +x /home/kali/ducky/plug_duck.sh
```

---

## ✅ Step 2: Create systemd Service

```bash
sudo nano /etc/systemd/system/duckyplug.service
```

**Paste this content:**

```ini
[Unit]
Description=Plug & Play Ducky Script on Boot
After=multi-user.target

[Service]
ExecStart=/home/kali/ducky/plug_duck.sh
WorkingDirectory=/home/kali/ducky
StandardOutput=journal
StandardError=journal
Restart=on-failure
User=root

[Install]
WantedBy=multi-user.target
```

---

## ✅ Step 3: Enable & Start Service

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable duckyplug.service
sudo systemctl start duckyplug.service
```

---

## ❗ Permission Fix for `/dev/hidg0`

Since the script accesses `/dev/hidg0`, it needs root permission.

**Option 1: Add udev rule**

```bash
sudo nano /etc/udev/rules.d/99-hid.rules
```

Add:

```bash
KERNEL=="hidg0", MODE="0666"
```

Then reload:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

**OR** just run the script as root using systemd (already done above).

---

## 🔄 Reboot & Test

```bash
sudo reboot
```

After reboot, your selected Ducky script will run automatically.

---

## ✅ Troubleshooting

Check logs:

```bash
journalctl -u duckyplug.service -e
```

Fix permissions if needed:

```bash
sudo chmod 666 /dev/hidg0
```

---

## 👨‍💻 Author

Made by **Tarun Sharma**  
2025
