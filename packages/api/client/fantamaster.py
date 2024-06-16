import os
import urllib.parse
from client import Client

class Api(Client):
  def __init__(self, args, public_api_url=None, tool_api_url=None) -> None:
    
    if public_api_url is None:
      public_api_url = args.get("FANTAMASTER_BASE_URL")

    if tool_api_url is None:
      tool_api_url = args.get("FANTAMASTER_TOOL_BASE_URL")
    
    super().__init__(public_api_url, tool_api_url)

    self.ENDPOINT_PLAYERS_LIST = args.get("ENDPOINT_PLAYERS_LIST")
    self.ENDPOINT_PLAYERS_UNAVAILABLE = args.get("ENDPOINT_PLAYERS_UNAVAILABLE")
    self.ENDPOINT_SYNTHETIC_STATS_THIS_SEASON = args.get("ENDPOINT_SYNTHETIC_STATS_THIS_SEASON")
    self.ENDPOINT_RATINGS = args.get("ENDPOINT_RATINGS")
    self.ENDPOINT_PROBABLE_LINEUPS = args.get("ENDPOINT_PROBABLE_LINEUPS")
    self.ENDPOINT_PLAYERS = args.get("ENDPOINT_PLAYERS")

  def get_available_apis(self, kind=""):
    return {}
  
  # Lista Giocatori attualmente in Serie A e utilizzabili per il fantacalcio
  # https://publicapi.fantamaster.it/playerslist/
  def playerslist(self, args={}):
    url = self.public_api_url + self.ENDPOINT_PLAYERS_LIST
    return self.make_request(url, payload=args)
  
  # Giocatori attualmente indisponibili (infortunati o squalificati)
  # https://publicapi.fantamaster.it/unavailable/
  def unavailable(self, args={}):
    url = self.public_api_url + self.ENDPOINT_PLAYERS_UNAVAILABLE
    return self.make_request(url,payload=args)

  # Statistiche sintetiche stagione corrente
  # https://publicapi.fantamaster.it/playersstats/
  def playersstats(self, args={}):
    url = self.public_api_url + self.ENDPOINT_SYNTHETIC_STATS_THIS_SEASON
    return self.make_request(url, payload=args)

  # Voti per ogni giornata
  #  https://publicapi.fantamaster.it/ratings/?day=27
  def ratings(self, args):
    url = self.public_api_url + self.ENDPOINT_RATINGS
    return self.make_request(url, payload=args)

  # Probabili formazioni prossima giornata
  # https://publicapi.fantamaster.it/lineups/
  def lineups(self, args):
    url = self.public_api_url + self.ENDPOINT_PROBABLE_LINEUPS
    return self.make_request(url, payload=args)
  
  # Dettaglio giocatore
  # https://publicapi.fantamaster.it/player/<player_name_slug>
  def playerdetail(self, args):
    url = self.tool_api_url + self.ENDPOINT_PLAYERS
    if not "player_name" in args:
      raise Exception("Player name not set")
    
    player_name_slug = self.make_slug(args["player_name"])
    url += urllib.parse.quote(player_name_slug) + "/"
    return self.make_request(url)

  def make_slug(self, player_name):
    return player_name.lower().replace(" ","-").replace("'","")  

  def main(args):
    pass