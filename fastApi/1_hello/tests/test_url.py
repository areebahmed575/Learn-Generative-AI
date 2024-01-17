import requests

r = requests.get('http://127.0.0.1:8000/hi/areeb%20ahmed')
def test_hi():
    
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'
    assert r.json() == 'Hello areeb ahmed'
    assert r.text == '"Hello areeb ahmed"'
