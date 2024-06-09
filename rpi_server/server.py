from flask import Flask, request, jsonify
import random
import secrets
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import hashlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii
app = Flask(__name__)

registering=''
logging=''
registerDone=False
loginDone=False
DB = {}
Q = {}
Q_Login = {}
flags = {
"ningwen"  : "Hi! Congratulation on your successful login!",
"team1": "The hustle and bustle of the city market was a symphony of sights and sounds.",
"team2": "The stars twinkled like diamonds scattered across the velvet night sky.",
"team3": "The scent of lavender in the garden brought a sense of calm and contentment.",
"team4": "The jazz band's rhythm set the pace for a night of dance and laughter.",
"team5": "The mountain's peak was crowned with snow, majestic against the blue sky.",
"team6": "The train whistle blew, a melancholy sound as it departed the station.",
"team7": "The potter's wheel hummed, spinning clay into a shape guided by gentle hands.",
"team8": "The vibrant murals on the city walls spoke volumes about its cultural tapestry.",
}
def decoder(data_str):
    data_bytes = base64.b64decode(data_str)
    return data_bytes

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        username = request.args.get('username')
        challenge = secrets.token_hex(16)
        Q[username] = {'challenge': challenge}
        return jsonify({'status': 'success', 'challenge': challenge})
    elif request.method == 'POST':
        data = request.json
        username = data['username']

        if username not in Q:
            return jsonify({'status': 'error', 'message': '請先使用GET拿取挑戰！'})

        signature = data["signature"].encode()
        public_key_pem = data["public_key"].encode()
        public_key = RSA.import_key(public_key_pem)
        credential_id = data['credential_id']
        challenge = Q[username]['challenge']
        print(public_key_pem)
        hash = SHA256.new(str.encode(challenge))
        verifier = PKCS115_SigScheme(public_key)
        try:
            verifier.verify(hash, decoder(signature))
            valid_signature = True
        except:
            valid_signature = False

        try:
            if valid_signature:
                DB[username] = {
                    'public_key': public_key_pem.decode(),
                    'credential_id': credential_id
                }
                print(DB)
                global registerDone
                registerDone=True
                return jsonify({'status': 'success', 'message': '註冊成功'})
            else:
                print(DB)
                return jsonify({'status': 'error', 'message': '驗證失敗'})
        except :
            print(DB)
            return jsonify({'status': 'error', 'message': '解密錯誤'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        username = request.args.get('username')
        if username in DB:
            challenge = secrets.token_hex(16)
            Q_Login[username] = {'challenge': challenge}
            return jsonify({'status': 'success', 'challenge': challenge, 'credential_id': DB[username]['credential_id']})
        else:
            return jsonify({'status': 'error', 'message': '使用者不存在'})

    elif request.method == 'POST':
        data = request.json
        username = data['username']

        if username not in Q_Login:
            return jsonify({'status': 'error', 'message': '請先使用GET拿取挑戰！'})

        signature = data["signature"].encode()
        public_key_pem = DB[username]["public_key"]
        public_key = RSA.import_key(public_key_pem)
        challenge = Q_Login[username]['challenge']
        hash = SHA256.new(str.encode(challenge))
        verifier = PKCS115_SigScheme(public_key)
        try:
            verifier.verify(hash, decoder(signature))
            valid_signature = True
        except:
            valid_signature = False
        
        print("valid_signature= ")
        print(valid_signature)

        try:
            if valid_signature:
                print(DB)
                print("成功")
                return jsonify({'status': 'success', 'message': '註冊成功', 'flag': username })
            else:
                print(DB)
                return jsonify({'status': 'error', 'message': '驗證失敗'})
        except :
            print(DB)
            return jsonify({'status': 'error', 'message': '解密錯誤'})
        
@app.route('/rpirequestreg', methods=['GET', 'POST'])
def rpirequestreg():
    if request.method == 'GET':
        global registering
        if registering != '':
            name=registering
            registering=''
            return jsonify({'status': 'success', 'pending': True, 'name': name})
        else:
            return jsonify({'status': 'success', 'pending': False})


@app.route('/frontendrequestreg', methods=['GET', 'POST'])
def frontendrequestreg():
    if request.method == 'GET':
        global registering
        username=request.args.get('username')
        registering=username
        return jsonify({'status': 'success', 'waiting': True})
    
@app.route('/frontendcheckreg', methods=['GET', 'POST'])
def frontendcheckreg():
    if request.method == 'GET':
        global registerDone
        if registerDone:
            registerDone=False
            return jsonify({'status': 'success', 'done': True,})
        else:
            return jsonify({'status': 'success', 'done': False})


if __name__ == '__main__':
    app.run(host='172.20.10.3', port=5000)