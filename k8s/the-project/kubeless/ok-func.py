import requests


def ok(event, context):
    url = "http://ok:8080/"
    response = requests.request("GET", url)

    return response.text
