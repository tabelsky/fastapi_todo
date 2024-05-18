import requests
import time
# resp = requests.post('http://localhost:8080/user', json={'username': 'admin', 'password': 'admin'})
# print(resp.text)
resp = requests.post('http://localhost:8080/login', json={'username': 'admin', 'password': 'admin'})
print(resp.text)


resp = requests.post('http://localhost:8080/todo', json={'title': 'Foo', 'description': 'The Foo Wrestlers'},
                     headers={'token': resp.json()['token']})

print(resp.text)