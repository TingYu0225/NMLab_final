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
import face_recognition
import numpy as np
from flask_cors import CORS, cross_origin
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
CORS(app)
registering = ''
logging = ''

registerDone = False
loginDone = False
pdfWaiting = False
rpiPDFactive = False
Q = {}
Q_Login = {}
DB = {}


signature = ''
public_key = ''
username = ''
filenames = []
pdfuser = ''
pdfreq = ''
pdfFile = ''


def decoder(data_str):
    data_bytes = base64.b64decode(data_str)
    return data_bytes


# Create arrays of known face encodings and their names
known_face_encodings = [

]
known_face_names = [

]


@app.route('/register', methods=['GET', 'POST'])
def register():
    global username
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

        global signature
        signature = data["signature"]
        global public_key
        public_key = data["public_key"]
        global registerDone
        registerDone = True
        # challenge = Q[username]['challenge']

        return jsonify({'status': 'success', 'message': '註冊成功'})


@app.route('/registerDB', methods=['GET'])
def registerDB():
    global username
    global signature
    global public_key
    return jsonify({'status': 'success', 'challenge':  Q[username]['challenge'], 'username': username, 'signature': signature, 'public_key': public_key})


@app.route('/pdfverify', methods=['GET', 'POST'])
def pdfverify():
    global username
    if request.method == 'GET':
        username = request.args.get('username')
        challenge = secrets.token_hex(16)
        Q_Login[username] = {'challenge': challenge}
        return jsonify({'status': 'success', 'challenge': challenge})

    elif request.method == 'POST':
        data = request.json
        username = data['username']
        global signature
        signature = data["signature"]
        global pdfWaiting
        pdfWaiting = True
        return jsonify({'status': 'success'})
        # challenge = Q_Login[username]['challenge']


@app.route('/pdfDB', methods=['GET', 'POST'])
def pdfDB():
    if request.method == 'GET':
        global username
        global signature
        global pdfreq
        return jsonify({'status': 'success', 'challenge':  Q_Login[username]['challenge'], 'username': username, 'signature': signature, 'filereq': pdfreq})
    if request.method == 'POST':
        data = request.json
        global pdfFile
        pdfFile = data["file"]
        return jsonify({'status': 'success'})


@app.route('/rpirequestreg', methods=['GET', 'POST'])
def rpirequestreg():
    if request.method == 'GET':
        global registering
        if registering != '':
            name = registering
            registering = ''
            return jsonify({'status': 'success', 'pending': True, 'name': name})
        else:
            return jsonify({'status': 'success', 'pending': False})


@app.route('/rpirequestpdf', methods=['GET', 'POST'])
def rpirequestpdf():
    if request.method == 'GET':
        global pdfreq
        global pdfuser
        global rpiPDFactive
        if rpiPDFactive:
            rpiPDFactive = False
            return jsonify({'status': 'success', 'pending': True, 'name': pdfuser})
        else:
            return jsonify({'status': 'success', 'pending': False})


@app.route("/frontendrequestreg", methods=["POST"])
@cross_origin()
def frontendrequestreg():
    if request.method == 'POST':
        return jsonify({'status': 'success', 'waiting': True})


@app.route("/DBcheckreg", methods=['GET', 'POST'])
def DBcheckreg():
    if request.method == 'GET':
        global registerDone
        if registerDone:
            registerDone = False
            return jsonify({'status': 'success', 'done': True, })
        else:
            return jsonify({'status': 'success', 'done': False})


@app.route("/DBcheckpdf", methods=['GET', 'POST'])
def DBcheckpdf():
    if request.method == 'GET':
        global pdfWaiting
        if pdfWaiting:
            pdfWaiting = False
            return jsonify({'status': 'success', 'waiting': True, })
        else:
            return jsonify({'status': 'success', 'waiting': False})


@app.route('/DBrequestlog', methods=['GET', 'POST'])
def DBrequestlog():
    if request.method == 'GET':
        global logging
        if logging != '':
            name = logging
            logging = ''
            return jsonify({'status': 'success', 'pending': True, 'name': name})
        else:
            return jsonify({'status': 'success', 'pending': False})
    if request.method == 'POST':
        data = request.json
        global filenames
        filenames = data["filenames"]
        global loginDone
        loginDone = True
        return jsonify({'status': 'success'})


@app.route('/frontendrequestlog', methods=['GET', 'POST'])
@cross_origin()
def frontendrequestlog():
    if request.method == 'POST':
        return jsonify({'status': 'success', 'waiting': True, 'username': "demo"})


@app.route('/frontendchecklog', methods=['GET', 'POST'])
@cross_origin()
def frontendchecklog():
    if request.method == 'GET':
        filenames = ["NewYear Gift", "Grimm's Fairy Tales"]
        loginDone = False
        time.sleep(3)
        return jsonify({'status': 'success', 'done': True, 'filenames': filenames})


@app.route('/pdfrequest', methods=['GET', 'POST'])
@cross_origin()
def pdfrequest():
    if request.method == 'POST':
        global pdfreq
        pdfreq = request.form.get('pdf')
        return jsonify({'status': 'success', 'waiting': True})

    if request.method == 'GET':
        time.sleep(5)
        global pdfreq
        fileString = ''
        if pdfreq == "NewYear Gift":
            with open("gift.pdf", "rb") as imageFile:
                fileString = base64.b64encode(imageFile.read())
                fileString = fileString.decode("utf-8")
        if pdfreq == "Grimm's Fairy Tales":
            with open("smith_chart.pdf", "rb") as imageFile:
                fileString = base64.b64encode(imageFile.read())
                fileString = fileString.decode("utf-8")

        return jsonify({'status': 'success', 'done': True, 'access': True, 'file': fileString})


if __name__ == "__main__":
    app.run(host='172.20.10.3', port=8080, debug=True)
