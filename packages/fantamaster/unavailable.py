#--web true
#--kind python:default
#--param FANTAMASTER_BASE_URL $FANTAMASTER_BASE_URL
#--param ENDPOINT_PLAYERS_UNAVAILABLE $ENDPOINT_PLAYERS_UNAVAILABLE

import requests

payload = {}
headers = {}

#this method return the unavailble players list for the current day
def main(args):

    url = args.get('FANTAMASTER_BASE_URL') + args.get('ENDPOINT_PLAYERS_UNAVAILABLE')

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)  
    print("response is", response.json())
    
    return {
        "body": response.json()
    }