from http.client import responses

import requests

url = 'http://127.0.0.1:5000/rest'

payload = {"params":{
            "command": "sum",
            "a":10,
            "b":20,
        }}

headers = {
    "Content-Type": "application/json"
}

response = requests.request('POST', url, json=payload, headers=headers)
print(response.text)










