# orig from @d4rkstar
from abc import ABC, abstractmethod
import requests
#import validators

class Client(ABC):

  # TBD: lista dei moduli API disponibili e relativi endpoint
  @abstractmethod
  def get_available_apis(self, kind=""):
    return {}

  def make_request(self, url, method="GET", headers={}, payload={}):
    try:
      response = requests.request(method, url, params=payload, headers=headers)
      print("Called url is " + response.request.url)
      #print("Called url is " + response.request.url +  " with status="+ f"{response.status_code}")
      #print("Resp is: " + repr(response.json()))
      if response.status_code == 200:
        return {"data": response.json(), "error": None, "code": None }
      
      return {"data": None, "error": "Http error", "code": response.status_code}
    except ConnectionError:
      return {"data": None, "error": "Connection Error", "code": response.status_code}      
    except Exception as e:
      return {"data": None, "error":"Error while sending request: " + f"{repr(e)}", "code": None },

  def __init__(self, public_api_url, tool_api_url) -> None:
    
    self.public_api_url = public_api_url
    self.tool_api_url = tool_api_url

    #valid= validators.url(public_api_url)
    #if valid: 
    #  self.public_api_url = public_api_url
    #else:
    #   raise Exception("Url invalid")

    #valid= validators.url(tool_api_url)
    #if valid: 
    #  self.tool_api_url = tool_api_url
    #else:
    #   raise Exception("Url invalid")

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

  
  
