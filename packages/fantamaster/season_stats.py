#--web true
#--kind python:default
#--param FANTAMASTER_BASE_URL $FANTAMASTER_BASE_URL
#--param ENDPOINT_SYNTHETIC_STATS_THIS_SEASON $ENDPOINT_SYNTHETIC_STATS_THIS_SEASON

import requests

payload = {}
headers = {}

def main(args):

    url = args.get('FANTAMASTER_BASE_URL') + args.get('ENDPOINT_SYNTHETIC_STATS_THIS_SEASON')

    payload = {}
    headers = {}

    print(url)

    response = requests.request("GET", url, headers=headers, data=payload)  
    print("response is", response.status_code)
    
    return {
        "body": response.json()
    }