import requests


def make_simple_http_request(url: str):
    resp = requests.get(url)
    json = resp.json()
    return json
