#--kind python:default
#--web true
#--param FANTAMASTER_BASE_URL $FANTAMASTER_BASE_URL
#--param ENDPOINT_PROBABLE_LINEUPS $ENDPOINT_PROBABLE_LINEUPS

import requests

payload = {}
headers = {}

def main(args):

    url = args.get('FANTAMASTER_BASE_URL') + args.get('ENDPOINT_PROBABLE_LINEUPS')

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)  
    print("response is", response.json())
    
    return {
        "body": response.json()
    }