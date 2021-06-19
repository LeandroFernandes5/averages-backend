import requests

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "index")
print(response)

coisas = requests.get(BASE + "login")
print(coisas.json())