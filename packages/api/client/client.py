import requests

class Client:

  # TBD: lista dei moduli API disponibili e relativi endpoint
  def get_available_apis(self, kind=""):
    return {}

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
