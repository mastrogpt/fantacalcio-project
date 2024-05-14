#--kind python:default
#--web true
#--param SPORTDB_BASE_URL $SPORTDB_BASE_URL
#--param ENDPOINT_ALL_LEAGUE $ENDPOINT_ALL_LEAGUE

import requests

payload = {}
headers = {}

def main(args):

    url = args.get('SPORTDB_BASE_URL') + args.get('ENDPOINT_ALL_LEAGUE')

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)  
    print("response is", response.json())
    
    return {
        "body": response.json()
    }