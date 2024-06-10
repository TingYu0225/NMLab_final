from flask import Flask, request, jsonify
#import random
# import secrets
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.backends import default_backend
#import hashlib
#import base64
# from Crypto.PublicKey import RSA
# from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
# from Crypto.Hash import SHA256
#import binascii
# import face_recognition
import numpy as np

app = Flask(__name__)

registering=''
logging=''
registerDone=False
loginDone=False
DB = {}
Q = {}
Q_Login = {}
@app.route('/frontendrequestreg',methods=['POST'])
def frontendrequestreg():
    if request.method == 'POST':
        print("2")
        username = request.form.get('username')
        print(username)
       
        #reg_image = face_recognition.load_image_file("dragon.jpg") #input image
        #reg_face_encoding = face_recognition.face_encodings(reg_image)[0]
        #global known_face_encodings
        #known_face_encodings.append(reg_face_encoding)
        #global known_face_names
        #known_face_names.append(username)
        global registering
        registering=username
        return jsonify({'status': 'success', 'waiting': True})
    
if __name__ == '__main__':
    app.run(host='172.20.10.5', port=8080)