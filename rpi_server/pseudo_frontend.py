import requests
import time

server_url = "http://172.20.10.3:5000"

if __name__ == "__main__":
    username = "B10901089"
    response = requests.get(f"{server_url}/frontendrequestreg", params={"username": username,}) #register
    data = response.json()
    print(data["waiting"])
    if data["waiting"]:
        while True:
            response = requests.get(f"{server_url}/frontendcheckreg", params={}) 
            data = response.json()
            if data["done"]:
                break
            time.sleep(1)
    print("OK")
    response = requests.get(f"{server_url}/frontendrequestlog", params={"username": username,}) #register
    data = response.json()
    print(data["waiting"])
    if data["waiting"]:
        while True:
            response = requests.get(f"{server_url}/frontendchecklog", params={}) 
            data = response.json()
            if data["done"]:
                break
            time.sleep(1)