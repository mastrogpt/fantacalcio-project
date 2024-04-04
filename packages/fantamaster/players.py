#--web true
#--kind python:default
#--param FANTAMASTER_BASE_URL $FANTAMASTER_BASE_URL
#--param ENDPOINT_PLAYERS_LIST $ENDPOINT_PLAYERS_LIST

import requests

payload = {}
headers = {}

#this method return the players list
def main(args):

    url = args.get('FANTAMASTER_BASE_URL') + args.get('ENDPOINT_PLAYERS_LIST')
    print(args.get('FANTAMASTER_BASE_URL'))
    print(args.get('ENDPOINT_PLAYERS_LIST'))
    print("url is ", url)
    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)  
    print("response is", response.json())
    return {
        "body": response.json()
        }
    