import  requests

r = requests.get("http://127.0.0.1:8000/todo/", ).json()
print(r) # {'item_id': 21}