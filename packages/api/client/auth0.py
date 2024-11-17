# import urllib.parse
# import json
# from os import environ as env
# from urllib.parse import quote_plus, urlencode

from client import Client
import json
from typing import Optional, Dict

class Api(Client):

  def __init__(self, args):
    self.headers = {}
    self.domain = args.get("AUTH0_DOMAIN")
    self.client_id = args.get("AUTH0_CLIENT_ID")
    self.client_secret = args.get("AUTH0_CLIENT_SECRET")
    self.app_audience = args.get("AUTH0_APP_AUDIENCE")
    self.token = None

  def authenticate(self, args) -> None:
    url = f"{self.domain}/oauth/token"
    payload = {
      "client_id": self.client_id,
      "client_secret": self.client_secret,
      "audience": self.app_audience,
      "grant_type": "client_credentials"
    }
    headers = {
      "content-type": "application/json"
    }
    response = self.make_request(url, 'POST', headers=headers, payload=payload, errorMessage='Authentication failed: ')
    self.token = response.get("data").get("access_token")
    self.headers = {
      "Authorization": f"Bearer {self.token}",
      "content-type": "application/json"
    }
    # to debug
    return response

  def get_users(self, args) -> Optional[Dict]:
    if not self.headers:
      # raise Exception("Unauthenticated. Call `authenticate` before making requests.")
      self.authenticate(args)
    url = f"{self.domain}/api/v2/users"
    headers = self.headers
    response = self.make_request(url, headers=headers, errorMessage='Error while retrieving users: ')
    return response

  def main(args):
    pass