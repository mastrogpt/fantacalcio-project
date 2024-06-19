from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class TeamDetails(Base):
    __tablename__ = 'team_details'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), unique=True, nullable=False)
    stadium_name = Column(String(255))
    stadium_city = Column(String(100))
    stadium_capacity = Column(Integer)
    stadium_img_url = Column(String(255))

    team = relationship("Team", back_populates="details")

    def __init__(self, team_id, stadium_name, stadium_city, stadium_capacity, stadium_img_url):
        self.team_id = team_id
        self.stadium_name = stadium_name
        self.stadium_city = stadium_city
        self.stadium_capacity = stadium_capacity
        self.stadium_img_url = stadium_img_url

    def __repr__(self):
        return f"<TeamDetails(id={self.id}, team_id={self.team_id}, stadium_name='{self.stadium_name}', stadium_city='{self.stadium_city}', stadium_capacity={self.stadium_capacity}, stadium_img_url='{self.stadium_img_url}')>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return TeamDetails.delete_handler(session, args)
        elif query_type == "insert":
            return TeamDetails.insert_handler(session, args)
        elif query_type == "upsert":
            return TeamDetails.upsert_handler(session, args)
        # elif query_type == "update":
        #     return TeamDetails.update_handler(session, args)
        else:
            return TeamDetails.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'details' in args:
                ret = TeamDetails.insert_if_not_exists(session, args['details'])
                if ret:
                    return {"statusCode": 200, "body": "Team details saved successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to save team details"}
            else:
                return {"statusCode": 400, "body": "No team details provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'details' in args:
                ret = TeamDetails.upsert(session, args['details'])
                if ret:
                    return {"statusCode": 200, "body": "Team details upserted successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert team details"}
            else:
                return {"statusCode": 400, "body": "No team details provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'team_id' in args:
            detail = TeamDetails.get_details_by_team_id(session, args['team_id'])
            return {"body": detail if detail else "Team details not found"}
        else:
            return {"body": TeamDetails.get_all_details(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'team_id' in args:
            return {"body": TeamDetails.delete_by_team_id(session, args['team_id'])}
        else:
            return {"body": TeamDetails.delete_all(session)}

    @staticmethod
    def delete_all(session):
        try:
            session.query(TeamDetails).delete()
            session.commit()
            return "All team details deleted"
        except Exception as e:
            print("Error while deleting team details:", e)
            session.rollback()
            return "Error while deleting team details"
        finally:
            session.close()

    @staticmethod
    def delete_by_team_id(session, team_id):
        try:
            detail = session.query(TeamDetails).filter_by(team_id=team_id).one()
            if detail:
                session.delete(detail)
                session.commit()
                return f"Details for team {team_id} deleted"
            else:
                return "Team details not found"
        except Exception as e:
            print("Error while deleting team details:", e)
            session.rollback()
            return "Error while deleting team details"
        finally:
            session.close()            

    @staticmethod
    def get_all_details(session):
        try:
            details = session.query(TeamDetails).all()
            return [detail._to_dict() for detail in details]
        except Exception as e:
            print("Error during team details loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def get_details_by_team_id(session, team_id):
        try:
            detail = session.query(TeamDetails).filter_by(team_id=team_id).one()
            return detail._to_dict() if detail else None
        except Exception as e:
            print("Error during team details loading:", e)
            return None
        finally:
            session.close()            

    @staticmethod
    def insert_if_not_exists(session, details):
        try:
            for detail in details:
                stmt = insert(TeamDetails).values(
                    team_id=detail['team_id'],
                    stadium_name=detail['stadium_name'],
                    stadium_city=detail['stadium_city'],
                    stadium_capacity=detail['stadium_capacity'],
                    stadium_img_url=detail['stadium_img_url']
                ).on_conflict_do_nothing(
                    index_elements=['team_id']
                )
                session.execute(stmt)
            session.commit()
            print("Team details saved successfully: ", [detail['team_id'] for detail in details])
            return True
        except Exception as e:
            print("Error during team details saving:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def upsert(session, details):
        try:
            for detail in details:
                stmt = insert(TeamDetails).values(
                    team_id=detail['team_id'],
                    stadium_name=detail['stadium_name'],
                    stadium_city=detail['stadium_city'],
                    stadium_capacity=detail['stadium_capacity'],
                    stadium_img_url=detail['stadium_img_url']
                ).on_conflict_do_update(
                    index_elements=['team_id'],
                    set_={
                        'stadium_name': detail['stadium_name'],
                        'stadium_city': detail['stadium_city'],
                        'stadium_capacity': detail['stadium_capacity'],
                        'stadium_img_url': detail['stadium_img_url']
                    }
                )
                session.execute(stmt)
            session.commit()
            print("Team details upserted successfully: ", [detail['team_id'] for detail in details])
            return True
        except Exception as e:
            print("Error during team details upserting:", e)
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'team_id': self.team_id,
            'stadium_name': self.stadium_name,
            'stadium_city': self.stadium_city,
            'stadium_capacity': self.stadium_capacity,
            'stadium_img_url': self.stadium_img_url
        }