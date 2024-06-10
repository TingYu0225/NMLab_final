import requests
import time
import hashlib
import base64
from tpm2_pytss.FAPI import FAPI

server_url = "http://172.20.10.3:8080"
fapi = FAPI()

def encoder(bytes_array):
    data_base64 = base64.b64encode(bytes_array)
    data_str = data_base64.decode('utf-8')
    return data_str

def hash_before_sign(data):
    sha256 = hashlib.sha256(data.encode('utf-8')).digest()
    return sha256

def register(username):
    # Step 1: Send a GET request with the desired username
    response = requests.get(f"{server_url}/register", params={"username": username})
    data = response.json()

    if data["status"] == "error":
        print(data["message"])
        return

    print("here")
    challenge = data["challenge"]
    # Step 2: Generate an RSA key pair (protected by password) and sign the challenge, please use hash_before_sign to hash the challenge before signing it.
    fapi.create_key("HS/SRK/"+username,"exportable")
    digest=hash_before_sign(challenge)
    signature,public_key,_=fapi.sign("HS/SRK/"+username, digest, "rsa_ssa")

    # Step 3: Send a POST request with the encrypted challenge, public key, and a sample credential_id
    post_data = {
        "username": username,
        "signature": encoder(signature),
        "public_key": public_key,
        "credential_id": "HS/SRK/"+username
    }

    response = requests.post(f"{server_url}/register", json=post_data)
    data = response.json()

    if data["status"] == "success":
        print("Registration Success!")
    else:
        print("Registration Failed!", data["message"])

def login(username):
    # Step 1: Send a GET request with the username
    response = requests.get(f"{server_url}/login", params={"username": username})
    data = response.json()

    if data["status"] == "error":
        print(data["message"])
        return

    challenge = data["challenge"]
    credential_id = data["credential_id"]
    print(data)

    # Step 2: Sign the challenge using the given key by credential_id.
    digest=hash_before_sign(challenge)
    signature,_,_=fapi.sign(credential_id,  digest, "rsa_ssa")

    # Step 3: Send a POST request with the encrypted challenge
    post_data = {
        "username": username,
        "signature": encoder(signature),
    }

    response = requests.post(f"{server_url}/login", json=post_data)
    data = response.json()

    if data["status"] == "success":
        print("Login Success!", data["flag"])
    else:
        print("Login Failed!", data["message"])

if __name__ == "__main__":
    username = "r11921a39"
    #register(username)
    #login(username)
    #response = requests.get(f"{server_url}/frontendrequestreg", params={"username": username,})
    #data = response.json()
    #print(data["waiting"])
    while(True):
        response = requests.get(f"{server_url}/rpirequestreg", params={})
        data2 = response.json()
        #print(data2["pending"])
        if data2["pending"]:
            register(data2["name"])
        time.sleep(1)

