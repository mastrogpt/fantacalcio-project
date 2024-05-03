import urllib.parse

from client import Client

class Api(Client):
  def __init__(self, public_api_url=None, tool_api_url=None) -> None:
    self.url = "https://httpbin.org/"
  
  def bin_get(self, args={}):
    url = self.url + "get"
    return self.make_request(url, payload=args)