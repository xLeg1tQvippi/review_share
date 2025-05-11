from flask import Flask, render_template, request, redirect, make_response
import subprocess
import webbrowser
import requests
import time
import qrcode


app = Flask(__name__)
@app.route('/')
def home():
    """ Render the home page. """
    return render_template('review.html')

@app.route('/go')
def go():
    url = request.args.get('to')
    response = make_response(redirect(url))
    response.headers['ngrok-skip-browser-warning'] = 'true'
    return response

def run_website_with_ngrok():
    ngrok = subprocess.Popen([r'C:\Users\User\Desktop\additional\ngrok\ngrok.exe', 'http', '5000'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2)


def get_public_url(retries=5, delay=2):
    for i in range(retries):
        try:
            res = requests.get("http://localhost:4040/api/tunnels").json()
            tunnels = res.get('tunnels', [])
            if tunnels:
                return tunnels[0]['public_url']
        except Exception as e:
            print(f"Ошибка получения туннеля: {e}")
        time.sleep(delay)
    raise RuntimeError("Ngrok туннель не найден.")

def generate_qr_code(url: str):
    filename = "ngrok_qr.png"
    qr = qrcode.make(url)
    qr.save(filename)
    print('QR code saved as', filename)
    

if __name__ == "__main__":
    run_website_with_ngrok()
    public_url = get_public_url(); print("public_url:", public_url)
    generate_qr_code(public_url)
    app.run(debug=True)