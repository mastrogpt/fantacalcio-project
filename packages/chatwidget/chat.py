#--web true
#--param FANTACALCIO_OPENAI_KEY $FANTACALCIO_OPENAI_KEY
#--param FANTACALCIO_ASSISTANT_ID $FANTACALCIO_ASSISTANT_ID
#--kind python:default

import openai
import requests
import time
import json
import traceback
class ChatBot: 

    def __init__(self, args):
        self.ASSISTANT_ID = args.get('FANTACALCIO_ASSISTANT_ID')
        self.api_key = args.get('FANTACALCIO_OPENAI_KEY')
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "OpenAI-Beta": "assistants=v2"
        }

    def create_thread(self):
        url = f"{self.base_url}/threads"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def post_message_on_thread(self, message, thread_id):
        url = f"{self.base_url}/threads/{thread_id}/messages"
        data = {
            "role": "user",
            "content": message
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()
    
    def list_messages(self, thread_id):
        url = f"{self.base_url}/threads/{thread_id}/messages"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def run_thread(self, thread_id):
        url = f"{self.base_url}/threads/{thread_id}/runs"
        data = {
            "assistant_id": self.ASSISTANT_ID
        }
        response = requests.post(url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()

    def run_thread_updates(self, thread_id, run_id):
        url = f"{self.base_url}/threads/{thread_id}/runs/{run_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        print("THREAD UPDATES: ", response.json())
        return response.json()

    def handle_tools(self, ai_response):
        required_action = ai_response['required_action']
        tool_calls = required_action['submit_tool_outputs']['tool_calls']
        
        tool_outputs = []
        for call in tool_calls:
            print("CALL IS", call)
            if call['function']['name'] == 'getPlayerStats':
                arguments = json.loads(call['function']['arguments'])
                surname = arguments['surname']
                team = arguments['team']
                
                url = "https://nuvolaris.dev/api/v1/web/fantatest/db/main?model=player&current_serie_a_players_filtered_by_surname_and_team"
                params = {'psurname': surname, 'team': team}
                player_stats = requests.get(url, params=params)
                result = player_stats.json()
                tool_outputs.append(
                    {
                        "tool_call_id": call['id'],
                        "output": str(result) if isinstance(result, dict) else str(result[0])
                    }
                )
            
        self.submit_tool_outputs(ai_response['thread_id'], ai_response['id'], tool_outputs)

    def submit_tool_outputs(self, thread_id, run_id, tool_outputs):
        try:
            url = f"{self.base_url}/threads/{thread_id}/runs/{run_id}/submit_tool_outputs"
            print("Calling GPT WITH URL", url)
            data = {
                "tool_outputs": tool_outputs
            }
            print("DATA SUBMITTING IS", json.dumps(data, indent=4))
            
            response = requests.post(url, headers=self.headers, json=data)
            print("RESPONSE OK")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                'body': {
                    'output': f'An error occurred: {repr(e)}'
                }
            }
                

def main(args):
    try:
        ai_instance = ChatBot(args)
        
        # check if thread already exists
        if args.get("thread_id") is None:
            thread = ai_instance.create_thread()
            thread_id = thread['id']
        else:
            thread_id = args.get("thread_id")

        ai_instance.post_message_on_thread(args.get('message'), thread_id)
        
        run_id = ai_instance.run_thread(thread_id)['id']
        
        timeout = 30 
        interval = 1 
        start_time = time.time()

        while True:
            ai_response = ai_instance.run_thread_updates(thread_id, run_id)
            thread_status = ai_response['status']
            if thread_status == 'in_progress':
                print('thread in progress')
                continue

            elif thread_status == 'requires_action':
                print('thread required action')
                ai_instance.handle_tools(ai_response)

            messages = ai_instance.list_messages(thread_id)


            if messages['data']:
                last_message = messages['data'][0]
                print("last message", messages)
                
                if last_message['role'] == 'assistant' and last_message['content']:
                    return {
                        'body': {
                            'output': last_message['content'],
                            'id': thread_id
                        }
                    }
            if time.time() - start_time > timeout:
                return {
                    'body': {
                        'output': 'Timeout: No response with content from assistant',
                        'id': thread_id
                    }
                }

            time.sleep(interval)

    except Exception as e:
        
        return {
            'body': {
                'output': f'An error occurred: {e}'
            }
        }
