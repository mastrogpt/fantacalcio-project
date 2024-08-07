#--web true
#--param OPENAI_API_HOST $OPENAI_API_HOST
#--param OPENAI_API_KEY $OPENAI_API_KEY
#--kind python:default

from openai import AzureOpenAI

ROLE = """
Usando circa 200 parole in formato markdown (h5 e p sono permessi):
Ti devi presentare con una frase ironica che ti descriva nel nostro sito MastroGPT. 
Sei un AI assistant che conosce tutti i segreti della serie A italiana e aiuterai gli utenti 
a vincere al fantacalcio. Lavori per Nuvolaris nel team MastroGPT.
"""

class Chatbot:

    MODEL = "gpt-4"
    

    def __init__(self, args):
        # accesso parametri
        key = args.get("OPENAI_API_KEY")
        host = args.get("OPENAI_API_HOST")
        # accesso alla ai
        ai = AzureOpenAI(api_version="2023-12-01-preview", api_key=key, azure_endpoint=host)
        self.ai = ai

    def ask(self, inp, role=ROLE):
        system = {"role": "system", "content": role}
        user = {"role": "user", "content": inp}
        request = [system, user]
        ai = self.ai
        comp = ai.chat.completions.create(model=self.MODEL, messages=request)
        if len(comp.choices) >0:
            return comp.choices[0].message.content
        return "I do not understand."


def main(args):
    print("going to ask infos to openai with apikey " + args.get('OPENAI_API_KEY'))
    print("and deployment " + args.get('OPENAI_API_HOST'))

    print(args.get('input'))
    chat = Chatbot(args)
    # read input
    inp = "chi sei e dove mi trovo?"
    # produce output
    out = chat.ask(inp)
    # prepare res
    res = {
        "output": out
    }
    return {
        "body": res
    }