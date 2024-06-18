from sqlalchemy import Column, Integer, String, Boolean, delete, create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    team_name = Column(String(50), unique=True, nullable=False)
    team_code = Column(String(10))
    team_country = Column(String(50))
    team_founded = Column(Integer)
    team_logo_url = Column(String(255))
    current_in_serie_a = Column(Boolean)
    apifootball_id = Column(Integer, unique=True)

    # players = relationship("Player", back_populates="team")
    # details = relationship("TeamDetails", back_populates="team")
    # team_name_mappings = relationship("TeamNameMapping", back_populates="team")

    def __init__(self, team_name, team_code, team_country, team_founded, team_logo_url, current_in_serie_a, apifootball_id):
        #self.uuid = uuid
        self.team_name = team_name
        self.team_code = team_code
        self.team_country = team_country
        self.team_founded = team_founded
        self.team_logo_url = team_logo_url
        self.current_in_serie_a = current_in_serie_a
        self.apifootball_id = apifootball_id
        
    def __repr__(self):
        return f"<Team(id={self.id}, team_name='{self.team_name}', team_code='{self.team_code}', team_country='{self.team_country}', team_founded={self.team_founded}, team_logo_url='{self.team_logo_url}', current_in_serie_a={self.current_in_serie_a}, apifootball_id={self.apifootball_id})>"

    @staticmethod
    def handler(session, args):

        query_type = args.get("query")
      
        if query_type == "delete":
            return Team.delete_handler(session, args)
        elif query_type == "new":
            if 'teams' in args:
                success = Team.save_teams(session, args['teams'])

                if success:
                    return {"statusCode": 200, "body": "Teams saved successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to save teams"}
            else:
                return {"statusCode": 400, "body": "No teams provided in the payload"}

        elif query_type == "update":
            return Team.update_handler(session, args)
        else:
            return Team.get_handler(session, args)

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})
            print("update_fields: {update_fields}")
            if 'id' in args:
                team_id = args['id']
                ret = Team.update_team_by_id(session, team_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for team with ID: {team_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for team with ID: {team_id}"}
            else:
                ret = Team.update_all_teams(session, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for all teams"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for all teams"}
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
        else:
            return {"body": Team.get_all_teams(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Team.delete_by_id(session, args['id'])}
        else:
            return {"body": Team.delete_all(session)}

    @staticmethod
    def get_all_teams(session):

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
    def save_teams(session, teams):  
        try:
            for team in teams:
                stmt = insert(Team).values(
                    team_name=team['team_name'],
                    team_code=team['team_code'],
                    team_country=team['team_country'],
                    team_founded=team['team_founded'],
                    team_logo_url=team['team_logo_url'],
                    current_in_serie_a=team['current_in_serie_a'],
                    apifootball_id=team['apifootball_id']
                ).on_conflict_do_nothing(
                    index_elements=['team_name']
                )
                session.execute(stmt)
            session.commit()
            print("Teams saved successfully: ", [team['team_name'] for team in teams]) 
            return True
        except Exception as e:
            print("Error during teams saving:", e)
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
            print("Error during team loading:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def get_team_by_apifootball_id(session, apifootball_id):
        try:
            team = session.query(Team).filter_by(apifootball_id=apifootball_id).one()
            return team._to_dict() if team else None
        except Exception as e:
            print("Error during team loading:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def update_team_by_id(session, team_id, update_fields):
        try:
            team = session.query(Team).filter_by(id=team_id).one()
            for field, value in update_fields.items():
                print(f"field: {field}, value: {value}")
                if hasattr(team, field):
                    setattr(team, field, value)
                else:
                    raise AttributeError(f"Field '{field}' does not exist in Team model")
            session.commit()
            return True
        except NoResultFound:
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
    def update_all_teams(session, update_fields):
        try:
            teams = session.query(Team).all()
            for team in teams:
                for field, value in update_fields.items():
                    print(f"field: {field}, value: {value}")
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
            'team_name': self.team_name,
            'team_code': self.team_code,
            'team_country': self.team_country,
            'team_founded': self.team_founded,
            'team_logo_url': self.team_logo_url,
            'current_in_serie_a': self.current_in_serie_a,
            'apifootball_id': self.apifootball_id
        }    
    