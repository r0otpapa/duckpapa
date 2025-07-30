from flask import Flask, render_template, request, jsonify
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'payloads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')k
def index():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/load', methods=['POST'])
def load():
    filename = request.form['filename']
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    return content

@app.route('/save', methods=['POST'])
def save():
    filename = request.form['filename']
    content = request.form['content']
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return 'Saved successfully'

@app.route('/delete', methods=['POST'])
def delete():
    filename = request.form['filename']
    path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(path):
        os.remove(path)
        return jsonify({'message': 'Deleted', 'files': os.listdir(UPLOAD_FOLDER)})
    else:
        return "File not found", 404

@app.route('/create', methods=['POST'])
def create():
    filename = request.form['filename']
    path = os.path.join(UPLOAD_FOLDER, filename)
    with open(path, 'w') as f:
        f.write("")
    files = os.listdir(UPLOAD_FOLDER)
    return jsonify({'message': 'Created', 'files': files})

@app.route('/rename', methods=['POST'])
def rename():
    old_name = request.form['oldname']
    new_name = request.form['newname']
    old_path = os.path.join(UPLOAD_FOLDER, old_name)
    new_path = os.path.join(UPLOAD_FOLDER, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        return jsonify({'message': 'Renamed', 'files': os.listdir(UPLOAD_FOLDER)})
    else:
        return "Original file not found", 404

@app.route('/run', methods=['POST'])
def run():
    filename = request.form['filename']
    script_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        subprocess.Popen(["python3", "duckpapa.py", script_path])
        return "Script running..."
    except Exception as e:
        return f"Error: {e}"

@app.route('/inject', methods=['POST'])
def inject():
    key = request.form.get('key', '').strip()
    if not key:
        return "No input provided", 400

    special_keys = {
        "ENTER": "ENTER", "SPACE": "SPACE", "CTRL": "CTRL",
        "ALT": "ALT", "GUI": "GUI", "ESC": "ESCAPE", "BACKSPACE": "BACKSPACE",
        "TAB": "TAB", "SHIFT": "SHIFT", "UP": "UPARROW", "DOWN": "DOWNARROW",
        "LEFT": "LEFTARROW", "RIGHT": "RIGHTARROW"
    }

    key_upper = key.upper()
    if key_upper in special_keys:
        payload = special_keys[key_upper]
    elif len(key) == 1:
        payload = f"STRING {key}"
    elif " " in key:
        payload = key_upper
    else:
        return f"[!] Unknown command: {key}", 400

    try:
        payload_path = os.path.join(UPLOAD_FOLDER, "temp_inject.txt")
        with open(payload_path, "w", encoding='utf-8') as f:
            f.write(payload + "\n")

        subprocess.Popen(["python3", "duckpapa.py", payload_path])
        return f"\u2705 Injected: {payload}"
    except Exception as e:
        return f"[!] Error injecting key: {e}", 500

@app.route("/plug", methods=["POST"])
def plug():
    import subprocess
    filename = request.form["filename"]
    script_path = os.path.abspath(f"payloads/{filename}")
    selected_file = "/home/usr/ducky/payloads/selected.txt"
    plug_script = "/home/usr/ducky/plug_duck.sh"
    service_name = "duckplug.service"

    # Ensure selected.txt is updated
    with open(selected_file, "w") as f:
        f.write(script_path)

    # Update plug_duck.sh
    with open(plug_script, "w") as f:
        f.write(f"#!/bin/bash\nsleep 5\npython3 /home/usr/ducky/duckpapa.py \"$(cat {selected_file})\"\n")
    os.chmod(plug_script, 0o755)

    # Toggle systemd service
    status = subprocess.getoutput(f"systemctl is-enabled {service_name}")
    if "enabled" in status:
        subprocess.call(["systemctl", "disable", service_name])
        return jsonify(message="? Plug & Play disabled at boot", enabled=False)
    else:
        subprocess.call(["systemctl", "enable", service_name])
        return jsonify(message="? Plug & Play enabled at boot", enabled=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
