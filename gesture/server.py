from flask import Flask, request
from threading import Thread

app = Flask(__name__)
use_keyboard = False

def is_keyboard_mode():
    global use_keyboard
    return use_keyboard

@app.route('/set_mode', methods=['POST'])
def set_mode():
    global use_keyboard
    mode = request.form.get('mode')
    if mode == 'normal':
        use_keyboard = False
    elif mode == 'keyboard':
        use_keyboard = True
    return 'Mode changed', 200

def start_server():
    server_thread = Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 5500})
    server_thread.daemon = True
    server_thread.start()