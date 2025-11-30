from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running fine!"

def start_web_server():
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000)).start()