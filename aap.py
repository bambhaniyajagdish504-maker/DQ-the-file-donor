from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "BOT IS RUNNING", 200

def start_web_server():
    app.run(host="0.0.0.0", port=8000)