from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey, Index, delete
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class League(Base):
    __tablename__ = 'leagues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    logo = Column(String(255))
    country_name = Column(String(100), nullable=False)
    country_code = Column(String(20))
    country_flag = Column(String(255))
    apifootball_id = Column(Integer, unique=True)

    seasons = relationship('Season', back_populates='league', cascade="all, delete-orphan")

    __table_args__ = (Index('ix_league_name_country_name', 'name', 'country_name', unique=True),)

    def __repr__(self):
        return f"<League(id={self.id}, uuid='{self.uuid}', name='{self.name}', logo='{self.logo}', country_name='{self.country_name}', country_code='{self.country_code}', country_flag='{self.country_flag}', apifootball_id={self.apifootball_id})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")

        if query_type == "delete":
            return League.delete_handler(session, args)
        elif query_type == "insert":
            return League.insert_handler(session, args)
        elif query_type == "upsert":
            return League.upsert_handler(session, args)
        elif query_type == "update":
            return League.update_handler(session, args)
        else:
            return League.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'leagues' in args:
                ret = League.insert_if_not_exists(session, args['leagues'])
                if ret:
                    return {"statusCode": 200, "body": "Leagues saved successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to save leagues"}
            else:
                return {"statusCode": 400, "body": "No leagues provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}            

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'leagues' in args:
                ret = League.upsert(session, args['leagues'])
                if ret:
                    return {"statusCode": 200, "body": "Leagues saved successfully"}
                else:
                    return {"statusCode": 500, "body": "Failed to save leagues"}
            else:
                return {"statusCode": 400, "body": "No leagues provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}                     

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'id' in args:
                league_id = args['id']
                ret = League.update_league_by_id(session, league_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for league with ID: {league_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for league with ID: {league_id}"}
            else:
                return {"statusCode": 400, "body": "No id param provided"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'id' in args:
            league = League.get_league_by_id(session, args['id'])
            return {"body": league if league else "League not found"}
        elif 'apifootball_id' in args:
            league = League.get_league_by_apifootball_id(session, args['apifootball_id'])
            return {"body": league if league else "League not found"}
        else:
            return {"body": League.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'id' in args:
            return {"body": League.delete_by_id(session, args['id'])}
        #FIXME delete_all 
        else:
            return {"body": League.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            leagues = session.query(League).all()
            return [league._to_dict() for league in leagues]
        except Exception as e:
            print("Error during leagues loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(League))
            session.commit()
            return "All leagues deleted"
        except Exception as e:
            print("Error while deleting leagues:", e)
            session.rollback()
            return "Error while deleting leagues"
        finally:
            session.close()

    @staticmethod
    def delete_by_id(session, league_id):
        try:
            league = session.query(League).get(league_id)
            if league:
                session.delete(league)
                session.commit()
                return f"League {league_id} deleted"
            else:
                return "League not found"
        except Exception as e:
            print("Error while deleting league:", e)
            session.rollback()
            return "Error while deleting league"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, leagues):  
        try:
            for league in leagues:
                stmt = insert(League).values(
                    uuid=league.get('uuid', str(uuid.uuid4())),
                    name=league['name'],
                    logo=league.get('logo'),
                    country_name=league['country_name'],
                    country_code=league.get('country_code'),
                    country_flag=league.get('country_flag'),
                    apifootball_id=league['apifootball_id']
                ).on_conflict_do_nothing(
                    index_elements=['name', 'country_name']
                )
                session.execute(stmt)
            session.commit()
            print("Leagues saved successfully: ", [league['name'] for league in leagues]) 
            return True
        except Exception as e:
            print("Error during leagues saving:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def upsert(session, leagues):
        try:
            for league in leagues:
                stmt = insert(League).values(
                    uuid=league.get('uuid', str(uuid.uuid4())),
                    name=league['name'],
                    logo=league.get('logo'),
                    country_name=league['country_name'],
                    country_code=league.get('country_code'),
                    country_flag=league.get('country_flag'),
                    apifootball_id=league['apifootball_id']
                ).on_conflict_do_update(
                    index_elements=['name', 'country_name'],
                    set_={
                        'logo': league.get('logo'),
                        'country_code': league.get('country_code'),
                        'country_flag': league.get('country_flag'),
                        'apifootball_id': league.get('apifootball_id')
                    }
                )
                session.execute(stmt)
            session.commit()
            print("Leagues upserted successfully: ", [league['name'] for league in leagues]) 
            return True
        except Exception as e:
            print("Error during leagues upserting:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_league_by_id(session, league_id):
        try:
            league = session.query(League).get(league_id)
            return league._to_dict() if league else None
        except Exception as e:
            print("Error during league loading:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def get_league_by_apifootball_id(session, apifootball_id):
        try:
            league = session.query(League).filter_by(apifootball_id=apifootball_id).one()
            return league._to_dict() if league else None
        except Exception as e:
            print("Error during league loading:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def update_league_by_id(session, league_id, update_fields):
        try:
            league = session.query(League).filter_by(id=league_id).one()
            for field, value in update_fields.items():
                if hasattr(league, field):
                    setattr(league, field, value)
                else:
                    raise AttributeError(f"Field '{field}' does not exist in League model")
            session.commit()
            return True
        except NoResultFound:
            return False
        except AttributeError as ae:
            print(f"AttributeError during update for league with ID {league_id}: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for league with ID {league_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'logo': self.logo,
            'country_name': self.country_name,
            'country_code': self.country_code,
            'country_flag': self.country_flag,
            'apifootball_id': self.apifootball_id
        }
