from sqlalchemy import Column, Integer, String, ForeignKey, PrimaryKeyConstraint, delete
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert 
from models.base import Base
import uuid

class CurrentPlayerTeam(Base):
    __tablename__ = 'current_players_teams'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    number = Column(Integer)
    position = Column(String(50))

    __table_args__ = (
        PrimaryKeyConstraint('team_id', 'player_id'),
    )

    team = relationship("Team", back_populates="current_players_teams")
    player = relationship("Player", back_populates="current_players_teams")

    def __init__(self, team_id, player_id, number, position):
        self.team_id = team_id
        self.player_id = player_id
        self.number = number
        self.position = position

    def __repr__(self):
        return f"<CurrentPlayerTeam(team_id={self.team_id}, player_id={self.player_id}, number={self.number}, position='{self.position}')>"        

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")

        if query_type == "delete":
            if 'team_id' in args and 'player_id' in args:
                return {"body": CurrentPlayerTeam.delete_by_id(session, args['team_id'], args['player_id'])}
            else:
                return {"body": CurrentPlayerTeam.delete_all(session)}
        elif query_type == "insert":
            if 'records' in args:
                ret = CurrentPlayerTeam.insert_if_not_exists(session, args['records'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to save records"}
            else:
                return {"statusCode": 400, "body": "No records provided in the payload"}
        else:
            if 'team_id' in args and 'player_id' in args:
                return {"body": CurrentPlayerTeam.get_record_by_id(session, args['team_id'], args['player_id'])}
            else:
                return {"body": CurrentPlayerTeam.get_all(session)}

    @staticmethod
    def insert_if_not_exists(session, records):
        try:
            inserted_records = []
            for record in records:
                stmt = insert(CurrentPlayerTeam).values(
                    team_id=record['team_id'],
                    player_id=record['player_id'],
                    number=record['number'],
                    position=record['position']
                ).on_conflict_do_nothing(
                    index_elements=['team_id', 'player_id']
                )
                result = session.execute(stmt)
                if result.rowcount > 0:  # If a row was actually inserted
                    inserted_record = session.query(CurrentPlayerTeam).filter_by(team_id=record['team_id'], player_id=record['player_id']).one()
                    inserted_records.append(inserted_record._to_dict())
            session.commit()
            return inserted_records
        except Exception as e:
            print("Error during records saving:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_all(session):
        try:
            records = session.query(CurrentPlayerTeam).all()
            return [record._to_dict() for record in records]
        except Exception as e:
            print("Error during records loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(CurrentPlayerTeam))
            session.commit()
            return "All records deleted"
        except Exception as e:
            print("Error while deleting records:", e)
            session.rollback()
            return "Error while deleting records"
        finally:
            session.close()

    @staticmethod
    def delete_by_id(session, team_id, player_id):
        try:
            record = session.query(CurrentPlayerTeam).filter_by(team_id=team_id, player_id=player_id).one()
            if record:
                session.delete(record)
                session.commit()
                return f"Record (team_id={team_id}, player_id={player_id}) deleted"
            else:
                return "Record not found"
        except Exception as e:
            print(f"Error while deleting record: {e}")
            session.rollback()
            return "Error while deleting record"
        finally:
            session.close()

    @staticmethod
    def get_record_by_id(session, team_id, player_id):
        try:
            record = session.query(CurrentPlayerTeam).filter_by(team_id=team_id, player_id=player_id).one()
            return record._to_dict() if record else None
        except Exception as e:
            print(f"Error during fetching record with team_id={team_id} and player_id={player_id}: {e}")
            return None
        finally:
            session.close()                

    def _to_dict(self):
        return {
            'uuid': self.uuid,
            'team_id': self.team_id,
            'player_id': self.player_id,
            'number': self.number,
            'position': self.position
        }

