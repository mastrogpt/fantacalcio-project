from abc import ABC, abstractmethod
import requests

class Client(ABC):

  # TBD: lista dei moduli API disponibili e relativi endpoint
  @abstractmethod
  def get_available_apis(self, kind=""):
    raise NotImplementedError()

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
      return {"data": None, "error":"Error while sending request: " + f"{repr(e)}", "code": None },

  def __init__(self, public_api_url, tool_api_url) -> None:

    if public_api_url is None or public_api_url.isspace():
      raise ValueError("Empty Url")
    else: self.public_api_url = public_api_url

    if tool_api_url is None or tool_api_url.isspace():
      raise ValueError("Empty Url")
    else: self.tool_api_url = tool_api_url

  # Lista Giocatori attualmente in Serie A e utilizzabili per il fantacalcio
  @abstractmethod
  def playerslist(self, args={}):
    pass
  
  # Giocatori attualmente indisponibili (infortunati o squalificati)
  @abstractmethod
  def unavailable(self, args={}):
    pass

  # Statistiche sintetiche stagione corrente
  @abstractmethod
  def playersstats(self, args={}):
    pass

  # Voti per ogni giornata
  @abstractmethod
  def ratings(self, args):
    pass

  # Probabili formazioni prossima giornata
  @abstractmethod
  def lineups(self, args):
    pass
  
  # Dettaglio giocatore
  @abstractmethod
  def playerdetail(self, args):
    pass
