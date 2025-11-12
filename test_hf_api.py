import requests

url = "https://praticks-stress-prediction-api.hf.space/predict"

response = requests.post(url, json={
    "X": -21.0,
    "Y": -53.0,
    "Z": 27.0,
    "EDA": 0.213944,
    "HR": 75.07,
    "TEMP": 30.37
})

print(response.json())