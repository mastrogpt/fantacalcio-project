#--kind python:default
#--web true
import requests
import urllib.parse

class FantamasterApi():
  def __init__(self, public_api_url, tool_api_url) -> None:
    self.public_api_url = public_api_url
    self.tool_api_url = tool_api_url

  def api(self, name: str, *args, **kwargs):
    do = f"{name}"
    if hasattr(self, do) and callable(getattr(self, do)):
        func = getattr(self, do)
        return func(*args, **kwargs) 

  def make_request(self, url, method="GET", headers={}, payload={}):
    try:
      response = requests.request(method, url, params=payload, headers=headers)
      print("Called url is " + response.request.url)
      if response.status_code == 200:
        return {"data": response.json(), "error": None, "code": None }
      
      return {"data": None, "error": "Http error", "code": response.status_code}
    except ConnectionError:
      return {"data": None, "error": "Connection Error", "code": response.status_code}      
    except Exception as e:
      return "Error while sending request: {repr(e)}",
  
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
  action = args.get("action")
  if action is None:
    return {"body": {"data": "Missing action", "error": True}}
  
  public_api_url = args.get("FANTAMASTER_PUBLIC_API_URL")
  if public_api_url is None:
    public_api_url = "https://publicapi.fantamaster.it/"

  tool_api_url = args.get("FANTAMASTER_TOOL_API_URL")
  if tool_api_url is None:
    tool_api_url = "https://tool-api.fantamaster.it/v1/"
  
  resp = ""
  cl = FantamasterApi(public_api_url, tool_api_url)
  
  del args["action"]
  try:
    resp = cl.api(action, args)
    if resp is None:
      return {"body": {"data": "Api not supported", "error": True }} 
    
    return {"body": resp}
  
  except Exception as e:
    return {"body": {"data": repr(e), "error": True}}
  
  
