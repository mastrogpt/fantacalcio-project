import urllib.parse

from client import Client

class Api(Client):
  def __init__(self, public_api_url=None, tool_api_url=None) -> None:
    self.url = self.SPORTDB_BASE_URL
    #"https://thesportsdb.com/api/v1/json/3/"

  # Lista leghe italiane
  # sportdb
  def leagueslist(self, args={}):
    url = self.url + self.ENDPOINT_ALL_LEAGUE #"search_all_leagues.php?c=Italy&s=Soccer"
    return self.make_request(url, payload=args)  
  
        #country_name_slug = self.make_slug(args["country_name"])
        #url += "search_all_leagues.php?c=" + urllib.parse.quote(country_name_slug) + "&s=Soccer/"

  def main(args):
    pass

  
  
