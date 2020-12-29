import requests
import json

content = {"dish_list": ["strogonoff", "pudim"]}
#content = json.dumps(content)
requests.post("http://0.0.0.0:5000/shoplist", json = content)