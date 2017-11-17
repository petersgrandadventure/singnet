import requests
r = requests.get("https://aigents.com/al/?rss%20ai")
print( r.status_code)
print(r.headers)
data = r.text
print(data)
print("Done")

