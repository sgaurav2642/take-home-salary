import requests

url = "http://127.0.0.1:5000/salary"

data = {
    "gross": 2380000,
    "variable": 100000,
    "tax_regime": "New",
    "section80c": 150000,
   "home_loan": 200000,
    "NPS2":10000,
    "rent_paid": 40000,
    "hra_received": 45000,
    "other_deduction3": 0
}

response = requests.post(url, json=data)
print(response.json())