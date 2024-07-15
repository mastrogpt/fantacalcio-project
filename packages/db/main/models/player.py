from sqlalchemy import Column, Integer, String, Boolean, Date, insert, UniqueConstraint, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql import insert as pg_insert
from models.season import Season
from models.team import Team
from models.current_player_team import CurrentPlayerTeam
from models.league import League
from models.player_season import PlayerSeason
from models.player_statistics import PlayerStatistics
from models.base import Base
from models.utils import Redis_utils
import uuid
from datetime import datetime

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    firstname = Column(String(100))
    lastname = Column(String(100))
    birth_date = Column(Date)
    birth_place = Column(String(100))
    birth_country = Column(String(100))
    nationality = Column(String(100))
    height = Column(String(20))
    weight = Column(String(20))
    injured = Column(Boolean)
    photo = Column(String(255))
    apifootball_id = Column(Integer, unique=True)

    __table_args__ = (
        UniqueConstraint('name', 'firstname', 'lastname', name='_name_firstname_lastname_uc'),
    )

    player_seasons = relationship('PlayerSeason', back_populates='player', cascade="all, delete-orphan")
    player_statistics = relationship('PlayerStatistics', back_populates='player', cascade="all, delete-orphan")
    current_players_teams = relationship('CurrentPlayerTeam', back_populates='player', cascade="all, delete-orphan")

    def __init__(self, name, firstname, lastname, birth_date, birth_place, birth_country, nationality, height, weight, injured, photo, apifootball_id):
        self.name = name
        self.firstname = firstname
        self.lastname = lastname
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.birth_country = birth_country
        self.nationality = nationality
        self.height = height
        self.weight = weight
        self.injured = injured
        self.photo = photo
        self.apifootball_id = apifootball_id

    def __repr__(self):
        return f"<Player(id={self.id}, name='{self.name}', firstname='{self.firstname}', lastname='{self.lastname}', birth_date={self.birth_date}, birth_place='{self.birth_place}', birth_country='{self.birth_country}', nationality='{self.nationality}', height='{self.height}', weight='{self.weight}', injured={self.injured}, photo='{self.photo}', apifootball_id={self.apifootball_id})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return Player.delete_handler(session, args)
        elif query_type == "insert":
            return Player.insert_handler(session, args)
        elif query_type == "upsert":
            return Player.upsert_handler(session, args)            
        elif query_type == "update":
            return Player.update_handler(session, args)
        else:
            return Player.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'players' in args:
                inserted_players = Player.insert_if_not_exists(session, args['players'])
                if inserted_players is not False:
                    return {"statusCode": 200, "body": inserted_players}
                else:
                    return {"statusCode": 500, "body": "Failed to save players"}
            else:
                return {"statusCode": 400, "body": "No players provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}
        finally:
            session.close()      

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'players' in args:
                ret = Player.upsert(session, args['players'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert players"}
            else:
                return {"statusCode": 400, "body": "No players provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}                     

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'id' in args:
                player_id = args['id']
                ret = Player.update_player_by_id(session, player_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for player with ID: {player_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for player with ID: {player_id}"}
            else:
                ret = Player.update_all(session, update_fields)
                if ret:
                    return {"statusCode": 200, "body": "Updated fields successfully for all players"}
                else:
                    return {"statusCode": 500, "body": "Failed to update fields for all players"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'id' in args:
            player = Player.get_player_by_id(session, args['id'])
            return {"body": player if player else "Player not found"}
        elif 'apifootball_id' in args:
            player = Player.get_player_by_apifootball_id(session, args['apifootball_id'])
            return {"body": player if player else "Player not found"}
        elif 'apifootball_ids' in args:
            apifootball_ids = list(map(int, args['apifootball_ids'].split(',')))
            players = Player.get_players_by_apifootball_ids(session, apifootball_ids)
            return {"body": players if players else "Players not found"}
        elif "current_serie_a_players" in args:
            current_serie_a_players = args.get("current_serie_a_players")
            if current_serie_a_players.lower() =="true":
                return {"body": Player.get_current_serie_a_players(session)}
            return {"statusCode": 500, "body": f"Value '{current_serie_a_players}' of current_serie_a_players param is not valid"} 
        elif "all_current_serie_a_players" in args:
            all_current_serie_a_players = args.get("all_current_serie_a_players")
            if all_current_serie_a_players.lower() =="true":
                return {"body": Player.get_all_current_serie_a_players(session,args)}
            return {"statusCode": 500, "body": f"Value '{all_current_serie_a_players}' of all_current_serie_a_players param is not valid"}                           
        else:
            return {"body": Player.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Player.delete_by_id(session, args['id'])}
        else:
            return {"body": Player.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            players = session.query(Player).all()
            return [player._to_dict() for player in players]
        except Exception as e:
            print("Error during players loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(Player))
            session.commit()
            return "All players deleted"
        except Exception as e:
            print("Error while deleting players:", e)
            session.rollback()
            return "Error while deleting players"
        finally:
            session.close()

    @staticmethod
    def delete_by_id(session, player_id):
        try:
            player = session.query(Player).get(player_id)
            if player:
                session.delete(player)
                session.commit()
                return f"Player {player_id} deleted"
            else:
                return "Player not found"
        except Exception as e:
            print("Error while deleting player:", e)
            session.rollback()
            return "Error while deleting player"
        finally:
            session.close()

    @staticmethod
    def _parse_date(date_str):
        if isinstance(date_str, str):
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return None
        return date_str

    @staticmethod
    def insert_if_not_exists(session, players):
        try:
            inserted_players = []
            for player in players:
                # Convertiamo le date nel formato corretto
                player['birth_date'] = Player._parse_date(player.get('birth_date'))

                # Check if the player with the same apifootball_id already exists
                existing_player = session.query(Player).filter_by(apifootball_id=player['apifootball_id']).first()
                if existing_player:
                    continue  # Skip the insert if a player with the same apifootball_id already exists

                stmt = pg_insert(Player).values(
                    name=player['name'],
                    firstname=player['firstname'],
                    lastname=player['lastname'],
                    birth_date=player['birth_date'],
                    birth_place=player['birth_place'],
                    birth_country=player['birth_country'],
                    nationality=player['nationality'],
                    height=player['height'],
                    weight=player['weight'],
                    injured=player['injured'],
                    photo=player['photo'],
                    apifootball_id=player['apifootball_id']
                ).on_conflict_do_nothing(
                    index_elements=['name', 'firstname', 'lastname']
                )
                result = session.execute(stmt)
                if result.rowcount > 0:  # Se una riga è stata effettivamente inserita
                    inserted_player = session.query(Player).filter_by(
                        name=player['name'],
                        firstname=player['firstname'],
                        lastname=player['lastname']
                    ).one()
                    inserted_players.append(inserted_player._to_dict())

            session.commit()
            return inserted_players
        except Exception as e:
            print("Error during players saving:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def upsert(session, players):
        try:
            upserted_players = []
            for player in players:
                # Convertiamo le date nel formato corretto
                player['birth_date'] = Player._parse_date(player.get('birth_date'))

                # Primo controllo sulla tripla (name, firstname, lastname)
                existing_player = session.query(Player).filter_by(
                    name=player['name'],
                    firstname=player['firstname'],
                    lastname=player['lastname']
                ).one_or_none()

                if existing_player:
                    # Aggiorna le informazioni del giocatore esistente
                    existing_player.birth_date = player['birth_date']
                    existing_player.birth_place = player['birth_place']
                    existing_player.birth_country = player['birth_country']
                    existing_player.nationality = player['nationality']
                    existing_player.height = player['height']
                    existing_player.weight = player['weight']
                    existing_player.injured = player['injured']
                    existing_player.photo = player['photo']
                    existing_player.apifootball_id = player['apifootball_id']
                    upserted_player = existing_player
                else:
                    # Secondo controllo sull'apifootball_id
                    existing_player = session.query(Player).filter_by(
                        apifootball_id=player['apifootball_id']
                    ).one_or_none()

                    if existing_player:
                        # Aggiorna le informazioni del giocatore esistente ma cambiando nome, cognome o secondo nome
                        existing_player.name = player['name']
                        existing_player.firstname = player['firstname']
                        existing_player.lastname = player['lastname']
                        existing_player.birth_date = player['birth_date']
                        existing_player.birth_place = player['birth_place']
                        existing_player.birth_country = player['birth_country']
                        existing_player.nationality = player['nationality']
                        existing_player.height = player['height']
                        existing_player.weight = player['weight']
                        existing_player.injured = player['injured']
                        existing_player.photo = player['photo']
                        upserted_player = existing_player
                    else:
                        # Inserisci un nuovo giocatore
                        new_player = Player(
                            name=player['name'],
                            firstname=player['firstname'],
                            lastname=player['lastname'],
                            birth_date=player['birth_date'],
                            birth_place=player['birth_place'],
                            birth_country=player['birth_country'],
                            nationality=player['nationality'],
                            height=player['height'],
                            weight=player['weight'],
                            injured=player['injured'],
                            photo=player['photo'],
                            apifootball_id=player['apifootball_id']
                        )
                        session.add(new_player)
                        upserted_player = new_player

                session.flush()  # Sincronizza i cambiamenti con il database
                upserted_players.append(upserted_player._to_dict())

            session.commit()
            return upserted_players
        except Exception as e:
            print("Error during upsert operation:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def get_player_by_id(session, player_id):
        try:
            player = session.query(Player).get(player_id)
            if player:
                return player._to_dict()
            else:
                return None
        except Exception as e:
            print("Error while fetching player by id:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def get_player_by_apifootball_id(session, apifootball_id):
        try:
            player = session.query(Player).filter_by(apifootball_id=apifootball_id).one()
            if player:
                return player._to_dict()
            else:
                return None
        except NoResultFound:
            return None
        except Exception as e:
            print("Error while fetching player by apifootball_id:", e)
            return None
        finally:
            session.close()

    @staticmethod
    def get_players_by_apifootball_ids(session, apifootball_ids):
        try:
            players = session.query(Player).filter(Player.apifootball_id.in_(apifootball_ids)).all()
            return [player._to_dict() for player in players]
        except Exception as e:
            print("Error while fetching players by apifootball_ids:", e)
            return []
        finally:
            session.close()  
   
    @staticmethod
    def get_current_serie_a_players(session):
        ''' 
        This query returns all Serie A current players with their respective season and team details.

        This method retrieves players who are currently active in Serie A teams, including their team
        information and statistics for the current season.

        Returns:
            A list of dictionaries, each containing player details along with team and season information.

        Raises:
            Exception: If there's an error during the data retrieval process.

        Notes:
            - The query ensures players are currently associated with Serie A teams.
            - It includes team name, logo, ID, season ID, and player statistics such as position.
            - Suitable for scenarios where you need up-to-date information on Serie A players in current teams.
        '''
        try:

            players_teams = (session.query(Player, Team, Season, PlayerStatistics)
                 .join(PlayerStatistics, Player.id == PlayerStatistics.player_id)
                 .join(PlayerSeason, Player.id == PlayerSeason.player_id)
                 .join(Season, PlayerSeason.season_id == Season.id)
                 .join(League, Season.league_id == League.id)
                 .join(CurrentPlayerTeam, Player.id == CurrentPlayerTeam.player_id)
                 .join(Team, CurrentPlayerTeam.team_id == Team.id)
                 .filter(
                     League.name == "Serie A",
                     League.country_name == "Italy",
                     Season.current == True
                 )
                 .all())

            result = []
            print("PLAYERS ARE", players_teams)

            for player in players_teams:
                player_dict = player.Player._to_dict()
                player_dict['team'] = player.Team.name
                player_dict['team_logo'] = player.Team.logo
                player_dict['team_id'] = player.Team.id
                player_dict['season_id'] = player.Season.id
                player_dict['position'] = player.PlayerStatistics.position
    
                #player_dict['statistics'] = player.PlayerStatistics._to_dict()
                
                result.append(player_dict)
            return result
        except Exception as e:
            print(f"Error during fetching Serie A players for current season: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A players for current season: {e}"}
        finally:
            session.close()    

    @staticmethod
    def get_all_current_serie_a_players(session, args):
        ''' 
        This query returns all Serie A current players for the current season.
    
        Retrieves all players who are registered for the current Serie A season, regardless of their
        current team status (whether they are transferred, released, etc.).
    
        Returns:
            A list of dictionaries, each containing player details.
    
        Raises:
            Exception: If there's an error during the data retrieval process.
    
        Notes:
            - The query fetches players associated with the Serie A league in the current season.
            - It does not guarantee that players are currently active in Serie A teams.
            - **Crucial for ETL process**: This method should not be modified as it populates the `player_statistics` table.
            - Suitable when you need a comprehensive list of players registered for the current Serie A season,
              irrespective of their current team affiliation.
        '''
        try:
            r = Redis_utils(args)
            redisKey = "get_all_current_serie_a_players"
            players = r.read(redisKey)
            
            if players != None:
                return [player for player in players]

            else:
                players = session.query(Player).join(PlayerSeason).join(Season).join(League).filter(
                    League.name == "Serie A",
                    League.country_name == "Italy",
                    Season.current == True
                ).all()

                playersToLoad = []
                [playersToLoad.append(player._to_dict()) for player in players]

                r.write(args, redisKey, playersToLoad)
                return [player._to_dict() for player in players]
        except Exception as e:
            print(f"Error during fetching Serie A players for current season: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A players for current season: {e}"}
        finally:
            session.close()                                  

    @staticmethod
    def update_player_by_id(session, player_id, update_fields):
        try:
            player = session.query(Player).get(player_id)
            if player:
                for key, value in update_fields.items():
                    setattr(player, key, value)
                session.commit()
                return True
            else:
                return False
        except Exception as e:
            print("Error while updating player by id:", e)
            session.rollback()
            return False
        finally:
            session.close()

    @staticmethod
    def update_all(session, update_fields):
        try:
            players = session.query(Player).all()
            for player in players:
                for key, value in update_fields.items():
                    setattr(player, key, value)
            session.commit()
            return True
        except Exception as e:
            print("Error while updating all players:", e)
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'id': self.id,
            'uuid': self.uuid,
            'name': self.name,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'birth_place': self.birth_place,
            'birth_country': self.birth_country,
            'nationality': self.nationality,
            'height': self.height,
            'weight': self.weight,
            'injured': self.injured,
            'photo': self.photo,
            'apifootball_id': self.apifootball_id
        }
