#--web true
#--kind python:default
#--param POSTGRES_URL $POSTGRES_URL
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.article import Article

def main(args):
   
    db = DbConnection()
    db.connect_to_db(args.get("POSTGRES_URL"))
    
    if(args.get("model") == "article"):
        return Article.handler(db.engine, args)
    else: 
        return {
        "body": "model and/or query not present"
    }
   
class DbConnection:
    engine = None
    session = None

    def connect_to_db(self, db_url):
        try:
            self.engine = create_engine(db_url)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            print("Connession to db ok.")
        except Exception as e:
            print("Error during db conn:", e)
