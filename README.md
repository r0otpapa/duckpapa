# 🧠 Deckey: Raspberry Pi HID Keyboard Gadget

This project turns your Raspberry Pi Zero/Zero W/4 into a USB HID keyboard (like a Rubber Ducky), capable of sending keystrokes to a connected PC. It includes:

- A Flask-based control web interface
- A test script for HID key injection
- USB HID gadget setup via `/dev/hidg0`

```bash
sudo bash setup_deckey_gadget.sh
sudo python3 test.py
```

## 📁 Files

- `duckey.py` – Main script to type keystrokes using HID
- `webui.py` – Flask web UI (e.g. for triggering payloads)
- `setup_deckey_gadget.sh` – One-time USB HID setup script

``` bash
sudo apt install python3-Flask
chmod +x duckey.py
sudo python3 webui.py

```
## Optional
Ngrok Setup
``` bash
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-stable-linux-arm.zip
unzip ngrok-stable-linux-arm.zip
sudo mv ngrok /usr/local/bin/
```
```bash
ngrok config add-authtoken <YOUR_AUTH_TOKEN>
```
```bash
ngrok http 8080
```
try This
``` bash
sudo python3 duckey /payloads/notepad.txt
```
![Screenshot_26-7-2025_13038_192 168 247 90](https://github.com/user-attachments/assets/a67ab291-e7f0-4570-ad9b-daeb1ea33ec4)
