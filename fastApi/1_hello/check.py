import requests

# r = requests.get('http://127.0.0.1:8000')

r = requests.get('http://127.0.0.1:8000/hi/areeb%20ahmed')
print(r.status_code)
print(r.headers)
print(r.json())
print(r.text)

# to run -->python check.py on a  seperate terminal after running uvicorn hello:app