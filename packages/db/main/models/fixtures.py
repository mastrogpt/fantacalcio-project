from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, Index, func, delete
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
from models.season import Season
from models.league import League
import uuid

class Fixture(Base):
    __tablename__ = 'fixtures'
    
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    season_id = Column(Integer, ForeignKey('seasons.id', ondelete='CASCADE'), nullable=False)
    league_round = Column(Integer, nullable=False)
    home_team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    away_team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    goals_home = Column(Integer)
    goals_away = Column(Integer)    
    referee = Column(String(50))
    event_datetime = Column(DateTime(timezone=True))
    venue_name = Column(String(100))
    venue_city = Column(String(50))
    status_long = Column(String(50))
    status_short = Column(String(10))
    status_elapsed = Column(Integer)
    last_update = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    apifootball_id = Column(Integer, unique=True)

    __table_args__ = (
        UniqueConstraint('season_id', 'league_round', 'home_team_id', 'away_team_id', name='_season_round_home_away_uc'),
    )

    season = relationship('Season', back_populates='fixtures')
    home_team = relationship('Team', foreign_keys=[home_team_id], back_populates='fixtures_home')
    away_team = relationship('Team', foreign_keys=[away_team_id], back_populates='fixtures_away')
    fixture_statistics = relationship('FixtureStatistics', back_populates='fixture', cascade='all, delete-orphan')


    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def __repr__(self):
        return f"<Fixture(id={self.id}, uuid='{self.uuid}', season_id={self.season_id}, league_round={self.league_round}, home_team_id={self.home_team_id}, away_team_id={self.away_team_id})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return Fixture.delete_handler(session, args)
        elif query_type == "insert":
            return Fixture.insert_handler(session, args)         
        elif query_type == "update":
            return Fixture.update_handler(session, args)
        elif query_type == "upsert":
            return Fixture.upsert_handler(session, args)
        else:
            return Fixture.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'fixtures' in args:
                ret = Fixture.insert_if_not_exists(session, args['fixtures'])
                if ret is not False:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "ERROR inserting Fixture"}
            else:
                return {"statusCode": 400, "body": "No fixtures provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'fixtures' in args:
                ret = Fixture.upsert(session, args['fixtures'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert fixtures"}
            else:
                return {"statusCode": 400, "body": "No fixtures provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'id' in args:
                fixture_id = args['id']
                update_fields['last_update'] = func.now()  # Aggiorniamo il campo last_update
                ret = Fixture.update_by_id(session, fixture_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for id: {fixture_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for id: {fixture_id}"}
            else:
                return {"statusCode": 400, "body": "id is required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'id' in args:
            fixture = Fixture.get_by_id(session, args['id'])
            return {"body": fixture if fixture else "Fixture not found"}
        elif 'league_id' in args and 'season' in args:
            fixtures = Fixture.get_fixtures_by_league_id_and_season(session, int(args['league_id']), int(args['season']))
            return {"body": fixtures}               
        else:
            return {"body": Fixture.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Fixture.delete_by_id(session, args['id'])}
        else:
            return {"body": Fixture.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            fixtures = session.query(Fixture).all()
            return [f._to_dict() for f in fixtures]
        except Exception as e:
            print("Error during fixtures loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def get_fixtures_by_league_id_and_season(session, league_id, season):
        """
        Fetches all fixtures for a specific league in a given season.
        
        Args:
            session (Session): The SQLAlchemy session used to connect to the database.
            league_id (int): The ID of the league to filter fixtures by.
            season (int): The year of the season to filter fixtures by.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a fixture 
                  of the specified league and season.
            dict: In case of an error, returns a dictionary with a status code and an error message.
        
        Notes:
        - **Crucial for ETL process**: This method should not be modified.
        """
        try:
            fixtures = session.query(Fixture).join(Season).join(League).filter(
                League.id == league_id,
                Season.year == season
            ).all()
            return [fixture._to_dict() for fixture in fixtures]
        except Exception as e:
            print(f"Error during fetching fixtures for league {league_id} and season {season}: {e}")
            return {"statusCode": 500, "body": f"Error during fetching fixtures for league {league_id} and season {season}: {e}"}
        finally:
            session.close()               

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(Fixture))
            session.commit()
            return "All fixtures deleted"
        except Exception as e:
            print("Error while deleting fixtures:", e)
            session.rollback()
            return "Error while deleting fixtures"
        finally:
            session.close()

    @staticmethod
    def delete_by_id(session, fixture_id):
        try:
            fixture = session.query(Fixture).filter_by(id=fixture_id).one_or_none()
            if fixture:
                session.delete(fixture)
                session.commit()
                return f"Fixture with id={fixture_id} deleted"
            else:
                return "Fixture not found"
        except Exception as e:
            print(f"Error while deleting Fixture: {e}")
            session.rollback()
            return "Error while deleting Fixture"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, fixtures):
        try:
            inserted_records = []
            for f in fixtures:
                existing_fixture = session.query(Fixture).filter_by(
                    season_id=f['season_id'],
                    league_round=f['league_round'],
                    home_team_id=f['home_team_id'],
                    away_team_id=f['away_team_id']
                ).first()

                if existing_fixture:
                    continue  # Salta l'inserimento se esiste già una fixture con le stesse chiavi

                # Creazione della query di insert
                stmt = insert(Fixture).values(
                    uuid=str(uuid.uuid4()),
                    referee=f.get('referee'),
                    event_datetime=f.get('event_datetime'),
                    venue_name=f.get('venue_name'),
                    venue_city=f.get('venue_city'),
                    status_long=f.get('status_long'),
                    status_short=f.get('status_short'),
                    status_elapsed=f.get('status_elapsed'),
                    season_id=f.get('season_id'),
                    league_round=f.get('league_round'),
                    home_team_id=f.get('home_team_id'),
                    away_team_id=f.get('away_team_id'),
                    goals_home=f.get('goals_home'),
                    goals_away=f.get('goals_away'),
                    last_update=func.now(),
                    apifootball_id=f.get('apifootball_id')
                ).on_conflict_do_nothing(index_elements=['season_id', 'league_round', 'home_team_id', 'away_team_id'])

                # Esecuzione della query
                session.execute(stmt)
                inserted_records.append(f)

            session.commit()
            return inserted_records  # Ritorna le fixture inserite correttamente
        except Exception as e:
            print("Error during fixtures saving:", e)
            session.rollback()
            return []
        finally:
            session.close()

    @staticmethod
    def upsert(session, fixtures):
        try:
            upserted_fixtures = []
            for f in fixtures:
                existing_fixture = session.query(Fixture).filter_by(
                    season_id=f['season_id'],
                    league_round=f['league_round'],
                    home_team_id=f['home_team_id'],
                    away_team_id=f['away_team_id']
                ).first()

                if existing_fixture:
                    # Se la fixture esiste già, aggiorna i campi specificati
                    update_fields = {
                        'referee': f.get('referee'),
                        'event_datetime': f.get('event_datetime'),
                        'venue_name': f.get('venue_name'),
                        'venue_city': f.get('venue_city'),
                        'status_long': f.get('status_long'),
                        'status_short': f.get('status_short'),
                        'status_elapsed': f.get('status_elapsed'),
                        'goals_home': f.get('goals_home'),
                        'goals_away': f.get('goals_away'),
                        'last_update': func.now(),
                        'apifootball_id': f.get('apifootball_id')
                    }
                    session.query(Fixture).filter_by(id=existing_fixture.id).update(update_fields)
                else:
                    # Altrimenti, inserisci una nuova fixture
                    stmt = insert(Fixture).values(
                        uuid=str(uuid.uuid4()),
                        referee=f.get('referee'),
                        event_datetime=f.get('event_datetime'),
                        venue_name=f.get('venue_name'),
                        venue_city=f.get('venue_city'),
                        status_long=f.get('status_long'),
                        status_short=f.get('status_short'),
                        status_elapsed=f.get('status_elapsed'),
                        season_id=f.get('season_id'),
                        league_round=f.get('league_round'),
                        home_team_id=f.get('home_team_id'),
                        away_team_id=f.get('away_team_id'),
                        goals_home=f.get('goals_home'),
                        goals_away=f.get('goals_away'),
                        last_update=func.now(),
                        apifootball_id=f.get('apifootball_id')
                    )
                    session.execute(stmt)

                upserted_fixtures.append(f)

            session.commit()
            return upserted_fixtures  # Ritorna le fixture aggiornate/inserite correttamente
        except Exception as e:
            print("Error during fixtures upsert:", e)
            session.rollback()
            return []
        finally:
            session.close()

    @staticmethod
    def get_by_id(session, fixture_id):
        try:
            fixture = session.query(Fixture).filter_by(id=fixture_id).one_or_none()
            return fixture._to_dict() if fixture else None
        except Exception as e:
            print(f"Error during fetching fixture for id={fixture_id}: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def update_by_id(session, fixture_id, update_fields):
        try:
            update_fields['last_update'] = func.now()  # Aggiorniamo il campo last_update
            session.query(Fixture).filter_by(id=fixture_id).update(update_fields)
            session.commit()
            return True
        except Exception as e:
            print(f"Error during updating fixture for id={fixture_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'season_id': self.season_id,
            'league_round': self.league_round,
            'home_team_id': self.home_team_id,
            'away_team_id': self.away_team_id,
            'goals_home': self.goals_home,
            'goals_away': self.goals_away,            
            'referee': self.referee,
            'event_datetime': self.event_datetime.isoformat() if self.event_datetime else None,
            'venue_name': self.venue_name,
            'venue_city': self.venue_city,
            'status_long': self.status_long,
            'status_short': self.status_short,
            'status_elapsed': self.status_elapsed,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'apifootball_id': self.apifootball_id
        }