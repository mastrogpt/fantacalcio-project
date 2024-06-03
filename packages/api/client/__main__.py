#--param FANTAMASTER_BASE_URL $FANTAMASTER_BASE_URL
#--param FANTAMASTER_TOOL_BASE_URL $FANTAMASTER_TOOL_BASE_URL
#--param ENDPOINT_PLAYERS $ENDPOINT_PLAYERS
#--param ENDPOINT_PLAYERS_LIST $ENDPOINT_PLAYERS_LIST
#--param ENDPOINT_PLAYERS_UNAVAILABLE $ENDPOINT_PLAYERS_UNAVAILABLE
#--param ENDPOINT_RATINGS $ENDPOINT_RATINGS
#--param ENDPOINT_RATING_BY_DAY $ENDPOINT_RATING_BY_DAY
#--param ENDPOINT_PROBABLE_LINEUPS $ENDPOINT_PROBABLE_LINEUPS
#--param ENDPOINT_SYNTHETIC_STATS_THIS_SEASON $ENDPOINT_SYNTHETIC_STATS_THIS_SEASON
#--param DETAIL_STATS_URL $DETAIL_STATS_URL
#--param DETAIL_PLAYERS_LIST $DETAIL_PLAYERS_LIST
#--param SPORTDB_BASE_URL $SPORTDB_BASE_URL
#--param ENDPOINT_ALL_LEAGUE $ENDPOINT_ALL_LEAGUE
#--param ENDPOINT_ALL_EVENTS $ENDPOINT_ALL_EVENTS
#--param ENDPOINT_SEARCH_TEAM $ENDPOINT_SEARCH_TEAM
#--param ENDPOINT_PLAYER_BY_NAME $ENDPOINT_PLAYER_BY_NAME
#--param ENDPOINT_ALL_TEAMS $ENDPOINT_ALL_TEAMS
#--param ENDPOINT_PLAYER_DETAILS $ENDPOINT_PLAYER_DETAILS
#--param ENDPOINT_EVENT_RESULTS $ENDPOINT_EVENT_RESULTS
#--param ENDPOINT_EVENTS_LEAGUE_BY_SEASON $ENDPOINT_EVENTS_LEAGUE_BY_SEASON
#--param ENDPOINT_PLAYER_CONTRACTS $ENDPOINT_PLAYER_CONTRACTS
#--param ENDPOINT_TABLE_BY_LEAGUE_AND_SEASON $ENDPOINT_TABLE_BY_LEAGUE_AND_SEASON

#--kind python:default
#--web true

import importlib
import os.path
import sys

def main(args):
  print("test")
  module_name = args.get("module")
  action = args.get("action")

  if action is None:
    return {"body": {"data": "Missing action", "error": True}}
  
  try:
    syspath = sys.path
    curpath = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, curpath)
    api_lib = importlib.import_module(module_name)
    class_ = getattr(api_lib, "Api")
    api = class_(args)
    
    resp = None

    del args["action"]
    try:
      #def api(self, name: str, *args, **kwargs):
      do = f"{action}"
      if hasattr(api, do) and callable(getattr(api, do)):
        func = getattr(api, do)
        resp = func(args)

      if resp is None:
        return {"body": {"data": "Api not supported", "error": True }} 
      
      return {"body": resp}
    
    except Exception as e:
      return {"body": {"data": repr(e), "error": True}}

  except Exception as e:
    return {"body": {"data": "Error: " + f"{repr(e)}" + " sys path is: " + f"{repr(syspath)}" + " - curpath is: " + f"{repr(curpath)}", "error": True}}


  
  