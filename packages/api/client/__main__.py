#--param AUTH0_CLIENT_ID $AUTH0_CLIENT_ID
#--param AUTH0_CLIENT_SECRET $AUTH0_CLIENT_SECRET
#--param AUTH0_DOMAIN $AUTH0_DOMAIN
#--param AUTH0_APP_AUDIENCE $AUTH0_APP_AUDIENCE

#--kind python:default
#--web true

import importlib
import os.path
import sys

def main(args):
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