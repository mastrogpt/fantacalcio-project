from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Index
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class Season(Base):
    __tablename__ = 'seasons'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    league_id = Column(Integer, ForeignKey('leagues.id', ondelete='CASCADE'), nullable=False)
    year = Column(Integer, nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    current = Column(Boolean)

    league = relationship('League', back_populates='seasons')
    team_seasons = relationship('TeamSeason', back_populates='season', cascade="all, delete-orphan")
    season_players = relationship('PlayerSeason', back_populates='season', cascade="all, delete-orphan")
    player_statistics = relationship('PlayerStatistic', back_populates='season', cascade="all, delete-orphan")

    __table_args__ = (Index('ix_league_year', 'league_id', 'year', unique=True),)

    def __repr__(self):
        return f"<Season(id={self.id}, uuid='{self.uuid}', league_id={self.league_id}, year={self.year}, start_date={self.start_date}, end_date={self.end_date}, current={self.current})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")

        if query_type == "delete":
            return Season.delete_handler(session, args)
        elif query_type == "insert":
            return Season.insert_handler(session, args)
        elif query_type == "upsert":
            return Season.upsert_handler(session, args)
        elif query_type == "update":
            return Season.update_handler(session, args)
        else:
            return Season.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'seasons' in args:
                ret = Season.insert_if_not_exists(session, args['seasons'])
                if ret:
                    return {"statusCode": 200, "body": "Seasons saved successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to save seasons"}
            else:
                return {"statusCode": 400, "body": "No seasons provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}            

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'seasons' in args:
                ret = Season.upsert(session, args['seasons'])
                if ret:
                    return {"statusCode": 200, "body": "Seasons saved successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to save seasons"}
            else:
                return {"statusCode": 400, "body": "No seasons provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}                     

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'id' in args:
                season_id = args['id']
                ret = Season.update_season_by_id(session, season_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for season with ID: {season_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for season with ID: {season_id}"}
            else:
                return {"statusCode": 400, "body": "No id param provided"}                    
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'id' in args:
            season = Season.get_season_by_id(session, args['id'])
            return {"body": season if season else "Season not found"}
        elif 'league_id' in args and 'year' in args:
            season = Season.get_season_by_league_and_year(session, args['league_id'], args['year'])
            return {"body": season if season else "Season not found"}
        else:
            return {"body": Season.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Season.delete_by_id(session, args['id'])}
        else:
            return {"body": Season.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            seasons = session.query(Season).all()
            return [season._to_dict() for season in seasons]
        except Exception as e:
            print("Error during seasons loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(Season))
            session.commit()
            return "All seasons deleted"
        except Exception as e:
            print("Error while deleting seasons:", e)
            session.rollback()
            return "Error while deleting seasons"
        finally:
            session.close()

    @staticmethod
    def delete_by_id(session, season_id):
        try:
            season = session.query(Season).get(season_id)
            if season:
                session.delete(season)
                session.commit()
                return f"Season {season_id} deleted"
            else:
                return "Season not found"
        except Exception as e:
            print("Error while deleting season:", e)
            session.rollback()
            return "Error while deleting season"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, seasons):  
        try:
            for season in seasons:
                stmt = insert(Season).values(
                    uuid=season.get('uuid', str(uuid.uuid4())),
                    league_id=season['league_id'],
                    year=season['year'],
                    start_date=season.get('start_date'),
                    end_date=season.get('end_date'),
                    current=season.get('current', False)
                ).on_conflict_do_nothing(
                    index_elements=['league_id', 'year']
                )
                session.execute(stmt)
            session.commit()
            print("Seasons saved successfully: ", [season['year'] for season in seasons]) 
            return True
        except Exception as e:
            print("Error during seasons saving:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def upsert(session, seasons):
        try:
            for season in seasons:
                stmt = insert(Season).values(
                    uuid=season.get('uuid', str(uuid.uuid4())),
                    league_id=season['league_id'],
                    year=season['year'],
                    start_date=season.get('start_date'),
                    end_date=season.get('end_date'),
                    current=season.get('current', False)
                ).on_conflict_do_update(
                    index_elements=['league_id', 'year'],
                    set_={
                        'start_date': season.get('start_date'),
                        'end_date': season.get('end_date'),
                        'current': season.get('current', False)
                    }
                )
                session.execute(stmt)
            session.commit()
            print("Seasons upserted successfully: ", [season['year'] for season in seasons]) 
            return True
        except Exception as e:
            print("Error during seasons upserting:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_season_by_id(session, season_id):
        try:
            season = session.query(Season).get(season_id)
            return season._to_dict() if season else None
        except Exception as e:
            print("Error during season loading:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def get_season_by_league_and_year(session, league_id, year):
        try:
            season = session.query(Season).filter_by(league_id=league_id, year=year).one()
            return season._to_dict() if season else None
        except Exception as e:
            print("Error during season loading:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def update_season_by_id(session, season_id, update_fields):
        try:
            season = session.query(Season).filter_by(id=season_id).one()
            for field, value in update_fields.items():
                if hasattr(season, field):
                    setattr(season, field, value)
                else:
                    raise AttributeError(f"Field '{field}' does not exist in Season model")
            session.commit()
            return True
        except NoResultFound:
            return False
        except AttributeError as ae:
            print(f"AttributeError during update for season with ID {season_id}: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for season with ID {season_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'league_id': self.league_id,
            'year': self.year,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'current': self.current
        }
