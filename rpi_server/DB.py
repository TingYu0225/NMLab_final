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
import requests
import time
import json


server_url = "http://172.20.10.3:8080"

DB = {}

filename=["NewYear Gift", "Grimm's Fairy Tales"]
author=['team2', 'team2']

def decoder(data_str):
    data_bytes = base64.b64decode(data_str)
    return data_bytes

def register(data):
        username = data["username"]
        signature = data["signature"].encode()
        public_key_pem = data["public_key"].encode()
        public_key = RSA.import_key(public_key_pem)
        challenge = data['challenge']
        hash = SHA256.new(str.encode(challenge))
        verifier = PKCS115_SigScheme(public_key)
        try:
            verifier.verify(hash, decoder(signature))
            valid_signature = True
            print("Register Success")
        except:
            valid_signature = False

        if valid_signature:
            DB[username] = {
                'public_key': public_key_pem.decode(),
            }
    
def giveyouPDF(data):
    username = data["username"]
    signature = data["signature"].encode()
    authorname=''
    global filename
    global author
    for i in range(len(filename)):
        if filename[i]==data["filereq"]:
            authorname=author[i]
    public_key_pem = DB[authorname]["public_key"]
    public_key = RSA.import_key(public_key_pem)
    challenge = data['challenge']
    hash = SHA256.new(str.encode(challenge))
    verifier = PKCS115_SigScheme(public_key)
    try:
        verifier.verify(hash, decoder(signature))
        valid_signature = True
    except:
        valid_signature = False
    
    print("valid_signature= ")
    print(valid_signature)

    fileString='fail'
    if valid_signature:
        if data["filereq"]=="NewYear Gift":
            with open("gift.pdf", "rb") as imageFile:
                fileString = base64.b64encode(imageFile.read())
                fileString = fileString.decode("utf-8")
        if data["filereq"]=="Grimm's Fairy Tales":
            with open("smith_chart.pdf", "rb") as imageFile:
                fileString = base64.b64encode(imageFile.read())
                fileString = fileString.decode("utf-8")
    jdata={"file": fileString}
    response = requests.post(f"{server_url}/pdfDB", json=jdata)



if __name__ == "__main__":
    while(True):
        response = requests.get(f"{server_url}/DBcheckreg", params={})
        data2 = response.json()
        #print(data2["pending"])
        if data2["done"]:
            response = requests.get(f"{server_url}/registerDB", params={})
            data = response.json()
            register(data)

        response = requests.get(f"{server_url}/DBrequestlog", params={})
        data2 = response.json()
        if data2["pending"]:
            files=[]
            for i in range(len(filename)):
                if author[i]==data2["name"]:
                    files.append(filename[i])
            response = requests.post(f"{server_url}/DBrequestlog", json={"filenames": files})

        response = requests.get(f"{server_url}/DBcheckpdf", params={})
        data2 = response.json()
        #print(data2["pending"])
        if data2["waiting"]:
            response = requests.get(f"{server_url}/pdfDB", params={})
            data = response.json()
            giveyouPDF(data)
        time.sleep(1)


        