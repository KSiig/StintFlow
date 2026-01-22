import requests

def get_tire_mgmt():
  url = "http://localhost:6397/rest/garage/UIScreen/TireManagement"
  headers = {
      "accept": "application/json",
  }

  response = requests.get(url, headers=headers)
  response.raise_for_status()  # raises if HTTP 4xx/5xx

  return response.json()
