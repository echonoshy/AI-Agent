# filename: fetch_issues.py

import requests
import json

def fetch_issues():
    url = "https://api.github.com/repos/microsoft/FLAML/issues"
    params = {
        "state": "open",
        "labels": "good first issue"
    }
    response = requests.get(url, params=params)
    print(response.text)

fetch_issues()