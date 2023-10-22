import requests
import json

url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/bridger"

payload = json.dumps({
  "action": "getstudents"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
