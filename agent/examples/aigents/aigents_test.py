import requests
r = requests.get("https://aigents.com/al/?rss%20ai")
print( r.status_code)
print(r.headers)
data1 = r.text
print(data1)
print("Done")

