import urllib.parse

from client import Client

class Api(Client):
  def __init__(self, public_api_url=None, tool_api_url=None) -> None:

    if public_api_url is None:
      public_api_url = "https://thesportsdb.com/api/v1/json/3/"

    self.public_api_url = public_api_url

  # Lista leghe italiane
  # 
  def playerslist(self, args={}):
    url = self.public_api_url + "search_all_leagues.php?c=Italy&s=Soccer"
    return self.make_request(url, payload=args)  
  
        #country_name_slug = self.make_slug(args["country_name"])
        #url += urllib.parse.quote(country_name_slug) + "/"

  def main(args):
    pass

  
  
