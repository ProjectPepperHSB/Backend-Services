import requests
import json

with open('needData.json') as file:
    data = json.load(file)

count = 0
for d in data["data"]["list"]:
    url = f'https://services.guide3d.com/route/cors/index.php?project=100011&start=L00P1133&end={d["point"]}&mode=M0000&redirect=duration&format=none'
    r = requests.get(url, allow_redirects=True)
    print(f'dis: {r.json()["distance"]}')
    print(f'time: {r.json()["duration"]}')


