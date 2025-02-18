import http.client

conn = http.client.HTTPSConnection("scrapeninja.p.rapidapi.com")

payload = '{"url":"https://news.ycombinator.com/"}'

headers = {
    'x-rapidapi-key': "d42dbed423mshd69f27217e2311bp11bd5cjsnc2b55ca495da",
    'x-rapidapi-host': "scrapeninja.p.rapidapi.com",
    'Content-Type': "application/json"
}

conn.request("POST", "/scrape", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
