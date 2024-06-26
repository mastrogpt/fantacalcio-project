from sqlalchemy import Column, Integer, String, Boolean, delete, create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
from models.season import Season
from models.league import League
from models.team_season import TeamSeason
import uuid

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), unique=True, nullable=False)
    code = Column(String(10))
    country = Column(String(100))
    founded = Column(Integer)
    national = Column(Boolean)
    logo = Column(String(255))
    venue_name = Column(String(100))
    venue_address = Column(String(255))
    venue_city = Column(String(100))
    venue_capacity = Column(Integer)
    venue_surface = Column(String(50))
    venue_image = Column(String(255))
    apifootball_id = Column(Integer, unique=True)

    team_seasons = relationship('TeamSeason', back_populates='team', cascade="all, delete-orphan")
    player_statistics = relationship('PlayerStatistic', back_populates='team', cascade="all, delete-orphan")
    current_players_teams = relationship('CurrentPlayerTeam', back_populates='team', cascade="all, delete-orphan")

    def __init__(self, name, code, country, founded, national, logo, venue_name, venue_address, venue_city, venue_capacity, venue_surface, venue_image, apifootball_id):
        self.name = name
        self.code = code
        self.country = country
        self.founded = founded
        self.national = national
        self.logo = logo
        self.venue_name = venue_name
        self.venue_address = venue_address
        self.venue_city = venue_city
        self.venue_capacity = venue_capacity
        self.venue_surface = venue_surface
        self.venue_image = venue_image
        self.apifootball_id = apifootball_id
        
    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}', code='{self.code}', country='{self.country}', founded={self.founded}, national={self.national}, logo='{self.logo}', venue_name='{self.venue_name}', venue_address='{self.venue_address}', venue_city='{self.venue_city}', venue_capacity={self.venue_capacity}, venue_surface='{self.venue_surface}', venue_image='{self.venue_image}', apifootball_id={self.apifootball_id})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return Team.delete_handler(session, args)
        elif query_type == "insert":
            return Team.insert_handler(session, args)
        elif query_type == "upsert":
            return Team.upsert_handler(session, args)            
        elif query_type == "update":
            return Team.update_handler(session, args)
        else:
            return Team.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'teams' in args:
                ret = Team.insert_if_not_exists(session, args['teams'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to save teams"}
            else:
                return {"statusCode": 400, "body": "No teams provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}                 

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'teams' in args:
                ret = Team.upsert(session, args['teams'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert teams"}
            else:
                return {"statusCode": 400, "body": "No teams provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}                   

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'id' in args:
                team_id = args['id']
                ret = Team.update_team_by_id(session, team_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for team with ID: {team_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for team with ID: {team_id}"}
            else:
                ret = Team.update_all(session, update_fields)
                if ret:
                    return {"statusCode": 200, "body": "Updated fields successfully for all teams"}
                else:
                    return {"statusCode": 500, "body": "Failed to update fields for all teams"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'id' in args:
            team = Team.get_team_by_id(session, args['id'])
            return {"body": team if team else "Team not found"}
        elif 'apifootball_id' in args:
            team = Team.get_team_by_apifootball_id(session, args['apifootball_id'])
            return {"body": team if team else "Team not found"}
        elif 'apifootball_ids' in args:
            apifootball_ids = [int(id) for id in args['apifootball_ids'].split(',')]
            teams = Team.get_teams_by_apifootball_ids(session, apifootball_ids)
            return {"body": teams}
        elif "current_serie_a_teams" in args:
            current_serie_a_teams = args.get("current_serie_a_teams")
            if current_serie_a_teams.lower() == "true":
                return {"body": Team.get_current_serie_a_teams(session)}
            return {"statusCode": 500, "body": f"Value '{current_serie_a_teams}' of current_serie_a_teams param is not valid"} 
        else:
            return {"body": Team.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Team.delete_by_id(session, args['id'])}
        else:
            return {"body": Team.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            teams = session.query(Team).all()
            return [team._to_dict() for team in teams]
        except Exception as e:
            print("Error during teams loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(Team))
            session.commit()
            return "All teams deleted"
        except Exception as e:
            print("Error while deleting teams:", e)
            session.rollback()
            return "Error while deleting teams"
        finally:
            session.close()

    @staticmethod
    def delete_by_id(session, team_id):
        try:
            team = session.query(Team).get(team_id)
            if team:
                session.delete(team)
                session.commit()
                return f"Team {team_id} deleted"
            else:
                return "Team not found"
        except Exception as e:
            print("Error while deleting team:", e)
            session.rollback()
            return "Error while deleting team"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, teams):
        try:
            inserted_teams = []
            for team in teams:
                stmt = insert(Team).values(
                    name=team['name'],
                    code=team['code'],
                    country=team['country'],
                    founded=team['founded'],
                    national=team['national'],
                    logo=team['logo'],
                    venue_name=team['venue_name'],
                    venue_address=team['venue_address'],
                    venue_city=team['venue_city'],
                    venue_capacity=team['venue_capacity'],
                    venue_surface=team['venue_surface'],
                    venue_image=team['venue_image'],
                    apifootball_id=team['apifootball_id']
                ).on_conflict_do_nothing(
                    index_elements=['name']
                )
                result = session.execute(stmt)
                if result.rowcount > 0:  # If a row was actually inserted
                    inserted_team = session.query(Team).filter_by(name=team['name']).one()
                    inserted_teams.append(inserted_team._to_dict())
            session.commit()
            return inserted_teams
        except Exception as e:
            print("Error during teams saving:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def upsert(session, teams):
        try:
            upserted_teams = []
            for team in teams:
                stmt = insert(Team).values(
                    name=team['name'],
                    code=team['code'],
                    country=team['country'],
                    founded=team['founded'],
                    national=team['national'],
                    logo=team['logo'],
                    venue_name=team['venue_name'],
                    venue_address=team['venue_address'],
                    venue_city=team['venue_city'],
                    venue_capacity=team['venue_capacity'],
                    venue_surface=team['venue_surface'],
                    venue_image=team['venue_image'],
                    apifootball_id=team['apifootball_id']
                ).on_conflict_do_update(
                    index_elements=['name'],
                    set_={
                        'code': team['code'],
                        'country': team['country'],
                        'founded': team['founded'],
                        'national': team['national'],
                        'logo': team['logo'],
                        'venue_name': team['venue_name'],
                        'venue_address': team['venue_address'],
                        'venue_city': team['venue_city'],
                        'venue_capacity': team['venue_capacity'],
                        'venue_surface': team['venue_surface'],
                        'venue_image': team['venue_image'],
                        'apifootball_id': team['apifootball_id']
                    }
                )
                session.execute(stmt)
                upserted_team = session.query(Team).filter_by(name=team['name']).one()
                upserted_teams.append(upserted_team._to_dict())
            session.commit()
            return upserted_teams
        except Exception as e:
            print("Error during teams upserting:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_team_by_id(session, team_id):
        try:
            team = session.query(Team).get(team_id)
            return team._to_dict() if team else None
        except Exception as e:
            print(f"Error during fetching team with ID {team_id}: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_team_by_apifootball_id(session, apifootball_id):
        try:
            team = session.query(Team).filter_by(apifootball_id=apifootball_id).one()
            return team._to_dict() if team else None
        except Exception as e:
            print(f"Error during fetching team with API football ID {apifootball_id}: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def get_teams_by_apifootball_ids(session, apifootball_ids):
        try:
            teams = session.query(Team).filter(Team.apifootball_id.in_(apifootball_ids)).all()
            return [team._to_dict() for team in teams]
        except Exception as e:
            print(f"Error while fetching teams by apifootball_ids: {e}")
            return []
        finally:
            session.close() 

    @staticmethod
    def get_current_serie_a_teams(session):
        try:
            teams = session.query(Team).join(TeamSeason).join(Season).join(League).filter(
                League.name == "Serie A",
                League.country_name == "Italy",
                Season.current == True
            ).all()
            return [team._to_dict() for team in teams]
        except Exception as e:
            print(f"Error during fetching Serie A teams for current season: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A teams for current season: {e}"}
        finally:
            session.close()                       

    @staticmethod
    def update_team_by_id(session, team_id, update_fields):
        try:
            team = session.query(Team).filter_by(id=team_id).one()
            for field, value in update_fields.items():
                if hasattr(team, field):
                    setattr(team, field, value)
                else:
                    raise AttributeError(f"Field '{field}' does not exist in Team model")
            session.commit()
            return True
        except NoResultFound:
            print(f"Team with ID {team_id} not found.")
            return False
        except AttributeError as ae:
            print(f"AttributeError during update for team with ID {team_id}: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for team with ID {team_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def update_all(session, update_fields):
        try:
            teams = session.query(Team).all()
            for team in teams:
                for field, value in update_fields.items():
                    if hasattr(team, field):
                        setattr(team, field, value)
                    else:
                        raise AttributeError(f"Field '{field}' is not a valid attribute for Team model")
            session.commit()
            return True
        except AttributeError as ae:
            print(f"AttributeError during update for all teams: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for all teams: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'code': self.code,
            'country': self.country,
            'founded': self.founded,
            'national': self.national,
            'logo': self.logo,
            'venue_name': self.venue_name,
            'venue_address': self.venue_address,
            'venue_city': self.venue_city,
            'venue_capacity': self.venue_capacity,
            'venue_surface': self.venue_surface,
            'venue_image': self.venue_image,
            'apifootball_id': self.apifootball_id
        }

