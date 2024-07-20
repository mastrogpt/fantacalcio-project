#--web true
#--param OPENAI_API_HOST $OPENAI_API_HOST
#--param OPENAI_API_KEY $OPENAI_API_KEY
#--kind python:default


from openai import AzureOpenAI

ROLE = """
Il tuo scopo è quello di dare consigli su un calciatore della serie A italiana, usando un tono informale e non didascalico. 
Ti verrano fornite delle informazioni e statistiche sul calciatore e tu dovrai analizzarle per offrire una stima dello stesso, offrendo consigli al fantallenatore.
Chiaramente, importante farlo in base al ruolo -> per un attaccante ci interessano i gol segnati, per un portiere i rigori parati / gol subiti, per un difensore le intercettazioni e via discorrendo. 
Sii coerente in questo. Ricorda che le giornate in un campionato di serie a sono 38, quindi se uno ha 38 presenza ha giocato sempre. 
Miraccomando, consigli mirati, non con il fare sapientone.

Ti verranno fornite statistiche su un calciatore, il report deve esser in formato markdown (ma solo gli elementi p, h5 e h6 sono concessi)
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
    print(args.get('input'))
    chat = Chatbot(args)
    # read input
    inp = "My input is a json that describe player stats. Please prepare for me a synthetic commment of this player in markdown, explaining this data. Focus on main data, not in height or weight or similar. If player has no games, he should not be considered as available. Use italian language, please. " + str(args.get("input"))
    # produce output
    out = chat.ask(inp)
    # prepare res
    res = {
        "output": out
    }
    return {
        "body": res
    }