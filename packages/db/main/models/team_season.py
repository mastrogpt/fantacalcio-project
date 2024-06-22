from sqlalchemy import Column, Integer, ForeignKey, String, create_engine, delete
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class TeamSeason(Base):
    __tablename__ = 'teams_seasons'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), primary_key=True)
    season_id = Column(Integer, ForeignKey('seasons.id', ondelete='CASCADE'), primary_key=True)

    team = relationship('Team', back_populates='team_seasons')
    season = relationship('Season', back_populates='team_seasons')

    def __repr__(self):
        return f"<TeamSeason(uuid={self.uuid}, team_id={self.team_id}, season_id={self.season_id})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
        if query_type == "delete":
            return TeamSeason.delete_handler(session, args)
        elif query_type == "insert":
            return TeamSeason.insert_handler(session, args)
        elif query_type == "update":
            return TeamSeason.update_handler(session, args)
        else:
            return TeamSeason.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'team_season' in args:
                ret = TeamSeason.insert_if_not_exists(session, args['team_season'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to save TeamSeason entry"}
            else:
                return {"statusCode": 400, "body": "No TeamSeason entry provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})
            keys = {'team_id': args.get('team_id'), 'season_id': args.get('season_id')}
            ret = TeamSeason.update_entry(session, keys, update_fields)
            if ret:
                return {"statusCode": 200, "body": "Updated fields successfully for TeamSeason entry"}
            else:
                return {"statusCode": 500, "body": "Failed to update fields for TeamSeason entry"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'team_id' in args and 'season_id' in args:
            entry = TeamSeason.get_entry(session, args['team_id'], args['season_id'])
            return {"body": entry if entry else "Entry not found"}
        else:
            return {"body": TeamSeason.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'team_id' in args and 'season_id' in args:
            return {"body": TeamSeason.delete_entry(session, args['team_id'], args['season_id'])}
        else:
            return {"body": TeamSeason.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            entries = session.query(TeamSeason).all()
            return [entry._to_dict() for entry in entries]
        except Exception as e:
            print("Error during loading entries:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(TeamSeason))
            session.commit()
            return "All TeamSeason entries deleted"
        except Exception as e:
            print("Error while deleting entries:", e)
            session.rollback()
            return "Error while deleting entries"
        finally:
            session.close()

    @staticmethod
    def delete_entry(session, team_id, season_id):
        try:
            entry = session.query(TeamSeason).filter_by(team_id=team_id, season_id=season_id).one()
            session.delete(entry)
            session.commit()
            return f"Entry (team_id={team_id}, season_id={season_id}) deleted"
        except NoResultFound:
            return "Entry not found"
        except Exception as e:
            print("Error while deleting entry:", e)
            session.rollback()
            return "Error while deleting entry"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, entries):
        try:
            inserted_entries = []
            for entry in entries:
                stmt = insert(TeamSeason).values(
                    #uuid=entry.get('uuid', str(uuid.uuid4())),
                    team_id=entry['team_id'],
                    season_id=entry['season_id']
                ).on_conflict_do_nothing(
                    index_elements=['team_id', 'season_id']
                )
                session.execute(stmt)
                inserted_entries.append(entry)
            session.commit()
            return inserted_entries
        except Exception as e:
            print("Error during saving entries:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_entry(session, team_id, season_id):
        try:
            entry = session.query(TeamSeason).filter_by(team_id=team_id, season_id=season_id).one()
            return entry._to_dict() if entry else None
        except Exception as e:
            print(f"Error during fetching entry with (team_id={team_id}, season_id={season_id}): {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def update_entry(session, keys, update_fields):
        try:
            entry = session.query(TeamSeason).filter_by(**keys).one()
            for field, value in update_fields.items():
                if hasattr(entry, field):
                    setattr(entry, field, value)
                else:
                    raise AttributeError(f"Field '{field}' does not exist in TeamSeason model")
            session.commit()
            return True
        except NoResultFound:
            return False
        except AttributeError as ae:
            print(f"AttributeError during update for entry with keys {keys}: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for entry with keys {keys}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'uuid': self.uuid,
            'team_id': self.team_id,
            'season_id': self.season_id
        }
