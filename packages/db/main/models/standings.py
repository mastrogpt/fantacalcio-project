from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, delete, func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class Standings(Base):
    __tablename__ = 'standings'
    
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    season_id = Column(Integer, ForeignKey('seasons.id', ondelete='CASCADE'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), primary_key=True)
    rank = Column(Integer)
    points = Column(Integer)
    form = Column(String(10))
    status = Column(String(50))
    played_all = Column(Integer)
    win_all = Column(Integer)
    draw_all = Column(Integer)
    lose_all = Column(Integer)
    goals_for_all = Column(Integer)
    goals_against_all = Column(Integer)
    played_home = Column(Integer)
    win_home = Column(Integer)
    draw_home = Column(Integer)
    lose_home = Column(Integer)
    goals_for_home = Column(Integer)
    goals_against_home = Column(Integer)
    played_away = Column(Integer)
    win_away = Column(Integer)
    draw_away = Column(Integer)
    lose_away = Column(Integer)
    goals_for_away = Column(Integer)
    goals_against_away = Column(Integer)
    last_update = Column(DateTime, default=func.now(), onupdate=func.now())

    season = relationship('Season', back_populates='standings')
    team = relationship('Team', back_populates='standings')

    def __init__(self, season_id, team_id, **kwargs):
        self.season_id = season_id
        self.team_id = team_id
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def __repr__(self):
        return f"<Standings(season_id={self.season_id}, team_id={self.team_id}, uuid='{self.uuid}')>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return Standings.delete_handler(session, args)
        elif query_type == "insert":
            return Standings.insert_handler(session, args)         
        elif query_type == "update":
            return Standings.update_handler(session, args)
        elif query_type == "upsert":
            return Standings.upsert_handler(session, args)
        else:
            return Standings.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'standings' in args:
                ret = Standings.insert_if_not_exists(session, args['standings'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "ERROR Standings" + ret}
            else:
                return {"statusCode": 400, "body": "No standings provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'standings' in args:
                ret = Standings.upsert(session, args['standings'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert standings"}
            else:
                return {"statusCode": 400, "body": "No standings provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'season_id' in args and 'team_id' in args:
                season_id = args['season_id']
                team_id = args['team_id']
                update_fields['last_update'] = func.now()  # Aggiorniamo il campo last_update
                ret = Standings.update_by_ids(session, season_id, team_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for season_id: {season_id}, team_id: {team_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for season_id: {season_id}, team_id: {team_id}"}
            else:
                return {"statusCode": 400, "body": "season_id and team_id are required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'season_id' in args and 'team_id' in args:
            standings = Standings.get_by_ids(session, args['season_id'], args['team_id'])
            return {"body": standings if standings else "Standings not found"}
        else:
            return {"body": Standings.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'season_id' in args and 'team_id' in args:
            return {"body": Standings.delete_by_ids(session, args['season_id'], args['team_id'])}
        else:
            return {"body": Standings.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            standings = session.query(Standings).all()
            return [s._to_dict() for s in standings]
        except Exception as e:
            print("Error during standings loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(Standings))
            session.commit()
            return "All standings deleted"
        except Exception as e:
            print("Error while deleting standings:", e)
            session.rollback()
            return "Error while deleting standings"
        finally:
            session.close()

    @staticmethod
    def delete_by_ids(session, season_id, team_id):
        try:
            standing = session.query(Standings).filter_by(season_id=season_id, team_id=team_id).one_or_none()
            if standing:
                session.delete(standing)
                session.commit()
                return f"Standings with season_id={season_id}, team_id={team_id} deleted"
            else:
                return "Standings not found"
        except Exception as e:
            print(f"Error while deleting Standings: {e}")
            session.rollback()
            return "Error while deleting Standings"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, standings):
        try:
            inserted_records = []
            for s in standings:
                stmt = insert(Standings).values(
                    uuid=str(uuid.uuid4()),
                    season_id=s['season_id'],
                    team_id=s['team_id'],
                    rank=s.get('rank'),
                    points=s.get('points'),
                    form=s.get('form'),
                    status=s.get('status'),
                    played_all=s.get('played_all'),
                    win_all=s.get('win_all'),
                    draw_all=s.get('draw_all'),
                    lose_all=s.get('lose_all'),
                    goals_for_all=s.get('goals_for_all'),
                    goals_against_all=s.get('goals_against_all'),
                    played_home=s.get('played_home'),
                    win_home=s.get('win_home'),
                    draw_home=s.get('draw_home'),
                    lose_home=s.get('lose_home'),
                    goals_for_home=s.get('goals_for_home'),
                    goals_against_home=s.get('goals_against_home'),
                    played_away=s.get('played_away'),
                    win_away=s.get('win_away'),
                    draw_away=s.get('draw_away'),
                    lose_away=s.get('lose_away'),
                    goals_for_away=s.get('goals_for_away'),
                    goals_against_away=s.get('goals_against_away'),
                    last_update=func.now()  # Popoliamo il campo last_update
                ).on_conflict_do_nothing(
                    index_elements=['season_id', 'team_id']
                )
                session.execute(stmt)
                inserted_records.append(s)
            session.commit()
            return [s for s in inserted_records]
        except Exception as e:
            print("Error during standings saving:", e)
            session.rollback()
            return []
        finally:
            session.close()

    @staticmethod
    def upsert(session, standings):
        try:
            upserted_standings = []
            for s in standings:
                stmt = insert(Standings).values(
                    uuid=str(uuid.uuid4()),
                    season_id=s['season_id'],
                    team_id=s['team_id'],
                    rank=s.get('rank'),
                    points=s.get('points'),
                    form=s.get('form'),
                    status=s.get('status'),
                    played_all=s.get('played_all'),
                    win_all=s.get('win_all'),
                    draw_all=s.get('draw_all'),
                    lose_all=s.get('lose_all'),
                    goals_for_all=s.get('goals_for_all'),
                    goals_against_all=s.get('goals_against_all'),
                    played_home=s.get('played_home'),
                    win_home=s.get('win_home'),
                    draw_home=s.get('draw_home'),
                    lose_home=s.get('lose_home'),
                    goals_for_home=s.get('goals_for_home'),
                    goals_against_home=s.get('goals_against_home'),
                    played_away=s.get('played_away'),
                    win_away=s.get('win_away'),
                    draw_away=s.get('draw_away'),
                    lose_away=s.get('lose_away'),
                    goals_for_away=s.get('goals_for_away'),
                    goals_against_away=s.get('goals_against_away'),
                    last_update=func.now()  # Popoliamo il campo last_update
                ).on_conflict_do_update(
                    index_elements=['season_id', 'team_id'],
                    set_=dict(
                        rank=s.get('rank'),
                        points=s.get('points'),
                        form=s.get('form'),
                        status=s.get('status'),
                        played_all=s.get('played_all'),
                        win_all=s.get('win_all'),
                        draw_all=s.get('draw_all'),
                        lose_all=s.get('lose_all'),
                        goals_for_all=s.get('goals_for_all'),
                        goals_against_all=s.get('goals_against_all'),
                        played_home=s.get('played_home'),
                        win_home=s.get('win_home'),
                        draw_home=s.get('draw_home'),
                        lose_home=s.get('lose_home'),
                        goals_for_home=s.get('goals_for_home'),
                        goals_against_home=s.get('goals_against_home'),
                        played_away=s.get('played_away'),
                        win_away=s.get('win_away'),
                        draw_away=s.get('draw_away'),
                        lose_away=s.get('lose_away'),
                        goals_for_away=s.get('goals_for_away'),
                        goals_against_away=s.get('goals_against_away'),
                        last_update=func.now()  # Aggiorniamo il campo last_update
                    )
                )
                session.execute(stmt)
                upserted_standings.append(s)
            session.commit()
            return [s for s in upserted_standings]
        except Exception as e:
            print("Error during standings upsert:", e)
            session.rollback()
            return []
        finally:
            session.close()

    @staticmethod
    def get_by_ids(session, season_id, team_id):
        try:
            standings = session.query(Standings).filter_by(season_id=season_id, team_id=team_id).all()
            return [s._to_dict() for s in standings]
        except Exception as e:
            print(f"Error during fetching standings for season_id={season_id}, team_id={team_id}: {e}")
            return []
        finally:
            session.close()

    @staticmethod
    def update_by_ids(session, season_id, team_id, update_fields):
        try:
            update_fields['last_update'] = func.now()  # Aggiorniamo il campo last_update
            session.query(Standings).filter_by(season_id=season_id, team_id=team_id).update(update_fields)
            session.commit()
            return True
        except Exception as e:
            print(f"Error during updating standings for season_id={season_id}, team_id={team_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'uuid': self.uuid,
            'season_id': self.season_id,
            'team_id': self.team_id,
            'rank': self.rank,
            'points': self.points,
            'form': self.form,
            'status': self.status,
            'played_all': self.played_all,
            'win_all': self.win_all,
            'draw_all': self.draw_all,
            'lose_all': self.lose_all,
            'goals_for_all': self.goals_for_all,
            'goals_against_all': self.goals_against_all,
            'played_home': self.played_home,
            'win_home': self.win_home,
            'draw_home': self.draw_home,
            'lose_home': self.lose_home,
            'goals_for_home': self.goals_for_home,
            'goals_against_home': self.goals_against_home,
            'played_away': self.played_away,
            'win_away': self.win_away,
            'draw_away': self.draw_away,
            'lose_away': self.lose_away,
            'goals_for_away': self.goals_for_away,
            'goals_against_away': self.goals_against_away,
            'last_update': self.last_update
        }
