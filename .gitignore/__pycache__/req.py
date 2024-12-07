import requests

# Start a session
session = requests.Session()

# Login to set session (replace with your login details)
url = "http://127.0.0.1:5000/input-mood"
data = {
    "sentence" : "Im feeling happy"
}

response = requests.post(url=url, json=data )
print(response.json())
