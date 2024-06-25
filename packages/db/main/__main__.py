#--web true
#--kind python:default
#--param POSTGRES_URL $POSTGRES_URL
from dataclasses import dataclass
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.utils import create_tables, drop_tables
from models.article import Article
from models.season import Season
from models.league import League
from models.team import Team
from models.team_season import TeamSeason
from models.player import Player
from models.player_season import PlayerSeason
from models.player_statistic import PlayerStatistic
from models.current_player_team import CurrentPlayerTeam


def main(args):

    db_url = args.get("POSTGRES_URL")
   
    db = DbConnection()
    db.connect_to_db(db_url)

    # drop_tables(db_url)
    create_tables(db_url)
    
    if(args.get("model") == "article"):
        return Article.handler(db.session, args)
    elif(args.get("model") == "season"):
        return Season.handler(db.session, args)
    elif(args.get("model") == "league"):
        return League.handler(db.session, args) 
    elif(args.get("model") == "team"):
        return Team.handler(db.session, args)
    elif(args.get("model") == "team_season"):
        return TeamSeason.handler(db.session, args)
    elif(args.get("model") == "player"):
        return Player.handler(db.session, args)    
    elif(args.get("model") == "player_season"):
        return PlayerSeason.handler(db.session, args)
    elif(args.get("model") == "player_statistic"):
        return PlayerStatistic.handler(db.session, args)                
    elif(args.get("model") == "current_player_team"):
        return CurrentPlayerTeam.handler(db.session, args)                                                                                               
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
