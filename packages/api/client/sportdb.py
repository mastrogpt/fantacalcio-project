import os
import urllib.parse

from client import Client

#doc: https://www.thesportsdb.com/free_sports_api

class Api(Client):
  def __init__(self, args, public_api_url=None, tool_api_url=None) -> None:
   #"https://thesportsdb.com/api/v1/json/3/"
    self.url = args.get("SPORTDB_BASE_URL")
    self.ENDPOINT_ALL_LEAGUE = args.get("ENDPOINT_ALL_LEAGUE")
    self.ENDPOINT_ALL_EVENTS = args.get("ENDPOINT_ALL_EVENTS")
    self.ENDPOINT_SEARCH_TEAM = args.get("ENDPOINT_SEARCH_TEAM")
    self.ENDPOINT_PLAYER_BY_NAME = args.get("ENDPOINT_PLAYER_BY_NAME")
    self.ENDPOINT_ALL_TEAMS = args.get("ENDPOINT_ALL_TEAMS")
    self.ENDPOINT_PLAYER_DETAILS = args.get("ENDPOINT_PLAYER_DETAILS")
    self.ENDPOINT_EVENT_RESULTS = args.get("ENDPOINT_EVENT_RESULTS")
    self.ENDPOINT_EVENTS_LEAGUE_BY_SEASON = args.get("ENDPOINT_EVENTS_LEAGUE_BY_SEASON")
    self.ENDPOINT_PLAYER_CONTRACTS = args.get("ENDPOINT_PLAYER_CONTRACTS")
    self.ENDPOINT_TABLE_BY_LEAGUE_AND_SEASON = args.get("ENDPOINT_TABLE_BY_LEAGUE_AND_SEASON")

  # Lista leghe italiane
  # sportdb
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=leagueslist
  """Endpoint che restituisce l'elenco delle competizioni di calcio italiane"""
  def leagueslist(self, args={}):
    url = self.url + self.ENDPOINT_ALL_LEAGUE #"search_all_leagues.php?c=Italy&s=Soccer"
    return self.make_request(url, payload=args) 

  """Endpoint che restituisce la classica di un campionanto in una determinata stagione"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=tableByLeagueAndSeason&idLeague=4332&season=2023-2024
  def tableByLeagueAndSeason(self, args={}):
    #l=4328&s=2020-2021
    idLeague = args.get("idLeague")
    season = args.get("season")
    url = self.url + self.ENDPOINT_TABLE_BY_LEAGUE_AND_SEASON + "l=" + idLeague + "&s" + season
    return self.make_request(url, payload=args) 

  """Endpoint che restutuisce l'elenco degli eventi associati ad una descrizione"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=events&descEvent=Milan_VS_Inter
  def events(self, args={}):
    #e=Arsenal_vs_Chelsea
    descEvent = args.get("descEvent")
    url = self.url + self.ENDPOINT_ALL_EVENTS + "e=" + descEvent
    return self.make_request(url, payload=args)
  
  """Endpoint che restituisce i dettagli di un evento"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=eventDetails&idEvent=652890
  def eventDetails(self, args={}):
    idEvent = args.get("idEvent")
    url = self.url + self.ENDPOINT_EVENT_RESULTS + "id=" + idEvent
    return self.make_request(url, payload=args)
  
  """Endpoint che restituisce gli eventi di una deterinata competizione e stagione"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=eventsLeagueSeason&idLeague=4506&season=2014-2015
  def eventsLeagueSeason(self, args={}):
    #id=4328&s=2014-2015
    idLeague = args.get("idLeague")
    season = args.get("season")
    url = self.url + self.ENDPOINT_EVENTS_LEAGUE_BY_SEASON + "id=" + idLeague + "&s" + season
    return self.make_request(url, payload=args)
  
  """Endpoint che restituisce i dettagli di una squadra di calcio sulla base del nome"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=searchTeam&teamName=Inter
  def searchTeam(self, args={}):
    #t=Milan
    teamName = args.get("teamName")
    url = self.url + self.ENDPOINT_SEARCH_TEAM + "t=" + teamName
    return self.make_request(url, payload=args)
  
  """Endpoint che restituisce le caratteristiche di un giocatore sulla base del nome"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=searchPlayerByName&playerName=Lautaro
  def searchPlayerByName(self, args={}):
    #p=Ronaldo
    playerName = args.get("playerName")
    url = self.url + self.ENDPOINT_PLAYER_BY_NAME + "p=" + playerName
    return self.make_request(url, payload=args)
  
  """Endpoint che restituisce le caratteristiche di un giocatore sulla base della squadra e del nome"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=searchPlayerByName&teamName=Milan&playerName=Leao
  def searchPlayerByNameAndTeam(self, args={}):
    #p=Ronaldo
    playerName = args.get("playerName")
    teamName = args.get("teamName")
    url = self.url + self.ENDPOINT_PLAYER_BY_NAME + "t=" + teamName + "&p=" + playerName
    return self.make_request(url, payload=args)
  
  """Endpoint che restituisce i dettagli di un giocatore"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=playerDetails&idPlayer=34239204
  def playerDetails(self, args={}):
    idPlayer = args.get("idPlayer")
    url = self.url + self.ENDPOINT_PLAYER_DETAILS + "id=" + idPlayer
    return self.make_request(url, payload=args) 
  
  """Endpoint che restituisce i dettagli sul contratto che ha un giocatore col proprio club"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=playerContracts&idPlayer=34148307
  def playerContracts(self, args={}):
    idPlayer = args.get("idPlayer")
    url = self.url + self.ENDPOINT_PLAYER_CONTRACTS + "id=" + idPlayer
    return self.make_request(url, payload=args) 
  
  """Endpoint che restituisce l'elenco delle squadre di Seria A"""
  #https://nuvolaris.dev/api/v1/web/tmarinelli/api/client?module=sportdb&action=allTeamSerieA
  def allTeamSerieA(self, args={}):
    url = self.url + self.ENDPOINT_ALL_TEAMS + "l=Italian%20Serie%20A"
    return self.make_request(url, payload=args) 
  


  def main(args):
    pass

  
  
