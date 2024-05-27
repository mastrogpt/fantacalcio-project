import os
import urllib.parse

from client import Client

class Api(Client):
  def __init__(self, args, public_api_url=None, tool_api_url=None) -> None:
    self.url = args.get("SPORTDB_BASE_URL")
    self.ENDPOINT_ALL_LEAGUE = args.get("ENDPOINT_ALL_LEAGUE")
    self.ENDPOINT_ALL_EVENTS = args.get("ENDPOINT_ALL_EVENTS")
    self.ENDPOINT_SEARCH_TEAM = args.get("ENDPOINT_SEARCH_TEAM")
    self.API_PROVA = args.get("API_PROVA")
    #"https://thesportsdb.com/api/v1/json/3/"

  # Lista leghe italiane
  # sportdb
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=leagueslist
  def leagueslist(self, args={}):
    url = self.url + self.ENDPOINT_ALL_LEAGUE #"search_all_leagues.php?c=Italy&s=Soccer"
    return self.make_request(url, payload=args)  
  
        #country_name_slug = self.make_slug(args["country_name"])
        #url += "search_all_leagues.php?c=" + urllib.parse.quote(country_name_slug) + "&s=Soccer/"

  def events(self, args={}):
    url = self.url + self.ENDPOINT_ALL_EVENTS 
    return self.make_request(url, payload=args)
  
  def searchTeam(self, args={}):
    url = self.url + self.ENDPOINT_SEARCH_TEAM 
    return self.make_request(url, payload=args)

  def prova(self):
      return "pippo"  

  def prova2(self):
    url = self.API_PROVA
    return self.make_request(url)
  
        #country_name_slug = self.make_slug(args["country_name"])
        #url += "search_all_leagues.php?c=" + urllib.parse.quote(country_name_slug) + "&s=Soccer/"

  def main(args):
    pass

  
  
