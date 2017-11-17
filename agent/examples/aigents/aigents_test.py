import http.client
conn = http.client.HTTPConnection("aigents.com")
conn.request("GET", "/al/?rss%20ai")
r1 = conn.getresponse()
print( r1.status, r1.reason)
data1 = r1.read()
print(data1)
conn.close()
print("Done")

