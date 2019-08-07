import json
from tornado.httpclient import HTTPClient

response = HTTPClient().fetch("https://www.howsmyssl.com/a/check").body.decode()
data = json.loads(response)
tls_version = data["tls_version"]

print(tls_version) #