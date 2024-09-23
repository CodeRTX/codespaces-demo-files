import requests

def get_questions(amount=15):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "type": "multiple"
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data["results"]
