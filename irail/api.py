import urllib.parse
import urllib.request
from urllib.request import Request


def make_request(method, parameters={}):
    parameters["format"] = "json"
    parameters["lang"] = "nl"

    query = urllib.parse.urlencode(parameters)
    request_url = f"https://api.irail.be/{method}/?{query}"
    print(request_url)
    request = Request(request_url)
    request.add_header(
        'user-agent', 'treintje-komt-zo/1.0; github.com/AntheSevenants/treintje-komt-zo')
    return urllib.request.urlopen(request).read()
