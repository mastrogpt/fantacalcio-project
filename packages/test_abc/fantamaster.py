# orig from @d4rkstar

import urllib.parse

from client import Client

class Api(Client):
  def __init__(self, public_api_url=r"https://publicapi.fantamaster.it/", tool_api_url=r"https://tool-api.fantamaster.it/v1/"):
    super().__init__(public_api_url, tool_api_url)

  def get_available_apis(self, kind=""):
    return {}

  # Lista Giocatori attualmente in Serie A e utilizzabili per il fantacalcio
  # https://publicapi.fantamaster.it/playerslist/
  def playerslist(self, args={}):
    url = self.public_api_url + "playerslist/"
    return self.make_request(url, payload=args)
  
  # Giocatori attualmente indisponibili (infortunati o squalificati)
  # https://publicapi.fantamaster.it/unavailable/
  def unavailable(self, args={}):
    url = self.public_api_url + "unavailable/"
    return self.make_request(url,payload=args)

  # Statistiche sintetiche stagione corrente
  # https://publicapi.fantamaster.it/playersstats/
  def playersstats(self, args={}):
    url = self.public_api_url + "playersstats/"
    return self.make_request(url, payload=args)

  # Voti per ogni giornata
  #  https://publicapi.fantamaster.it/ratings/?day=27
  def ratings(self, args):
    url = self.public_api_url + "ratings/"
    return self.make_request(url, payload=args)

  # Probabili formazioni prossima giornata
  # https://publicapi.fantamaster.it/lineups/
  def lineups(self, args):
    url = self.public_api_url + "lineups/"
    return self.make_request(url, payload=args)
  
  # Dettaglio giocatore
  # https://publicapi.fantamaster.it/player/<player_name_slug>
  def playerdetail(self, args):
    url = self.tool_api_url + "players/"
    if not "player_name" in args:
      raise Exception("Player name not set")
    
    player_name_slug = self.make_slug(args["player_name"])
    url += urllib.parse.quote(player_name_slug) + "/"
    return self.make_request(url)

  def make_slug(self, player_name):
    return player_name.lower().replace(" ","-").replace("'","")  

  def main(args):
    pass

  
  