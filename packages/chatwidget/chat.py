#--web true
#--param FANTACALCIO_OPENAI_KEY $FANTACALCIO_OPENAI_KEY
#--param FANTACALCIO_ASSISTANT_ID $FANTACALCIO_ASSISTANT_ID
#--kind python:default

import openai
import requests
import time

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
        #print("thread runned with run id: " , response.json()['id'])
        #run_id = response.data.id
        response.raise_for_status()
        return response.json()

    def run_thread_updates(self, thread_id, run_id):
        url = f"{self.base_url}/threads/{thread_id}/runs/{run_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

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
            thread_status = ai_instance.run_thread_updates(thread_id, run_id)['status']
            if thread_status == 'in_progress':
                print('thread in progress')
            elif thread_status == 'requires_action':
                print('thread required action')
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
