import traceback
from models.fixtures import Fixture
from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, insert, UniqueConstraint, delete, or_, and_, case, cast, String, func, desc, asc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import aliased
from models.season import Season
from models.team import Team
from models.current_player_team import CurrentPlayerTeam
from models.league import League
from models.player_season import PlayerSeason
from models.team_season import TeamSeason
from models.player_statistics import PlayerStatistics
from models.fixture_player_statistics import FixturePlayerStatistics
from models.standings import Standings
from models.base import Base
from models.utils import Redis_utils
import uuid
from datetime import datetime, date
import json

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
    fixture_player_statistics = relationship('FixturePlayerStatistics', back_populates='player', cascade="all, delete-orphan")

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
        elif query_type == "stats":
            return Player.stats_handler(session, args)
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
                return {"body": Player.get_current_serie_a_players(session,args)}
            return {"statusCode": 500, "body": f"Value '{current_serie_a_players}' of current_serie_a_players param is not valid"} 
        elif "all_current_serie_a_players" in args:
            all_current_serie_a_players = args.get("all_current_serie_a_players")
            if all_current_serie_a_players.lower() =="true":
                return {"body": Player.get_all_current_serie_a_players(session)}
            return {"statusCode": 500, "body": f"Value '{all_current_serie_a_players}' of all_current_serie_a_players param is not valid"} 
        elif "current_serie_a_players_filtered_by_surname_and_team" in args:
                return {"body": Player.current_serie_a_players_filtered_by_surname_and_team(session,args)}
        elif 'league_id' in args and 'season' in args:
            return {"body": Player.get_players_by_league_id_and_season(session,int(args['league_id']), int(args['season']))}               
        return {"body": Player.get_all(session,args)}
    
    @staticmethod
    def stats_handler(session, args):
        if 'assist_man' in args:
            player = Player.best_assist_man(session, args)
            return {"body": player if player else "Player not found"}

        elif 'top_players_by_team_and_role' in args:
            player = Player.top_players_by_team_and_role(session, args)
            return {"body": player if player else "Player not found"}

        elif 'get_player_fixtures_stats' in args:

          season = args['season'] if 'season' in args and args['season'] else None
          player_name = args['player_name']
          last_n_rounds =  args['last_n_rounds'] if 'last_n_rounds' in args and args['last_n_rounds'] else None
          home_away_filter = args['home_away_filter'] if 'home_away_filter' in args and args['home_away_filter'] else None

          player_statistic_by_params = Player.get_player_fixtures_stats(session, player_name, last_n_rounds, home_away_filter, season)

          return {"body": player_statistic_by_params if player_statistic_by_params else "Players FIxtures Statistics not found"}
        elif 'get_upcoming_match_and_stats_for_players' in args:
            players_stats = Player.get_upcoming_match_and_stats_for_players(session, args)
            return {"body": players_stats if players_stats else "Players not found"}
        return {"body": Player.get_all(session,args)}
    

    @staticmethod
    def delete_handler(session, args):
        if 'id' in args:
            return {"body": Player.delete_by_id(session, args['id'])}
        else:
            return {"body": Player.delete_all(session)}

    @staticmethod
    def get_all(session,args):
        try:
            r = Redis_utils(args)
            redisKey = Player.get_all.__name__
            players = r.read(redisKey)
            
            if players != None:
                return [player for player in players]

            else:
                players = session.query(Player).all()

                playersToLoad = []
                [playersToLoad.append(player._to_dict()) for player in players]

                r.write(args, redisKey, playersToLoad)
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
    def get_players_by_name(session, player_name, isSubquery = False):

      player_names = player_name.split()
      firstName = player_names[0]

      secondName = ' '.join([str(name) for name in player_names if name != firstName])
      inverted_player_name = secondName + ' ' + firstName

      try:
        player_sub_query = (
          session.query(Player)
          .filter(or_(
            and_(func.unaccent(Player.name).ilike(func.unaccent(f"%{player_name}%"))),

            and_(func.unaccent(Player.name).ilike(func.unaccent(f"%{inverted_player_name}%"))),

            and_(func.unaccent(func.concat(Player.firstname, ' ', Player.lastname)).ilike(func.unaccent(f"%{player_name}%"))),

            and_(func.unaccent(func.concat(Player.lastname, ' ', Player.firstname)).ilike(func.unaccent(f"%{player_name}%"))),

            and_(
              func.unaccent(func.concat(Player.firstname)).ilike(func.unaccent(f"%{firstName}%")),

              func.unaccent(func.concat(Player.lastname)).ilike(func.unaccent(f"%{secondName}%"))
            ),

            and_(
              func.unaccent(func.concat(Player.lastname)).ilike(func.unaccent(f"%{firstName}%")),

              func.unaccent(func.concat(Player.firstname)).ilike(func.unaccent(f"%{secondName}%"))
            )
          ))
          .order_by(Player.lastname)
          .subquery()
        )

        if not isSubquery:
          result_query = session.query(player_sub_query)
          player_query = result_query.all()

          results = []
          columns = [column['name'] for column in result_query.column_descriptions]

          for row in player_query:
            player_dict = {}
            for attr in columns:
              if attr:
                player_dict[attr] = getattr(row, attr)

            results.append(player_dict)
            return results

      except Exception as e:
        print("Error while fetching player by id:", e)
        return None
      finally:
        if not isSubquery:
          session.close()

      return player_sub_query

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
    def get_current_serie_a_players(session, args):
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
            r = Redis_utils(args)
            redisKey = Player.get_current_serie_a_players.__name__
            players = r.read(redisKey)
    
            if players is not None:
                return [player for player in players]
    
            else:
                # Subquery to get current Serie A season IDs
                subquery = session.query(Season.id).join(League).filter(
                    League.name == "Serie A",
                    League.country_name == "Italy",
                    Season.current == True
                ).subquery()
                
                # Convert subquery into a select() construct
                select_subquery = session.query(subquery.c.id)
                
                # Main query to fetch player details
                players_teams = (session.query(
                        Player,
                        Team,
                        Season,
                        CurrentPlayerTeam.number,
                        CurrentPlayerTeam.position
                    )
                    .join(CurrentPlayerTeam, Player.id == CurrentPlayerTeam.player_id)
                    .join(Team, CurrentPlayerTeam.team_id == Team.id)
                    .join(TeamSeason, Team.id == TeamSeason.team_id)
                    .join(Season, TeamSeason.season_id == Season.id)
                    .filter(
                        TeamSeason.season_id.in_(select_subquery),
                        CurrentPlayerTeam.number.isnot(None)
                    )
                    .all())
                
                result = []
                
                for player, team, season, number, position in players_teams:
                    player_dict = player._to_dict()
                    player_dict['team'] = team.name
                    player_dict['team_logo'] = team.logo
                    player_dict['team_id'] = team.id
                    player_dict['season_id'] = season.id
                    player_dict['number'] = number
                    player_dict['position'] = position
                    
                    result.append(player_dict)
                
                r.write(args, redisKey, result)
                return result
        except Exception as e:
            print(f"Error during fetching Serie A players for current season: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A players for current season: {e}"}
        finally:
            session.close()

    @staticmethod
    def get_all_current_serie_a_players(session):
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
            players = session.query(Player).join(PlayerSeason).join(Season).join(League).filter(
                League.name == "Serie A",
                League.country_name == "Italy",
                Season.current == True
            ).all()
            return [player._to_dict() for player in players]
        except Exception as e:
            print(f"Error during fetching Serie A players for current season: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A players for current season: {e}"}
        finally:
            session.close()               

    @staticmethod
    def get_players_by_league_id_and_season(session, league_id, season):
        """
        Fetches all players for a specific league in a given season.
        
        Args:
            session (Session): The SQLAlchemy session used to connect to the database.
            league_id (int): The ID of the league to filter players by.
            season (int): The year of the season to filter players by.
        
        Returns:
            list: A list of dictionaries, where each dictionary represents a player 
                  of the specified league and season.
            dict: In case of an error, returns a dictionary with a status code and an error message.
        
        Notes:
        - **Crucial for ETL process**: This method should not be modified.
        """
        try:
            players = session.query(Player).join(PlayerSeason).join(Season).join(League).filter(
                League.id == league_id,
                Season.year == season
            ).all()
            return [player._to_dict() for player in players]
        except Exception as e:
            print(f"Error during fetching players for league {league_id} and season {season}: {e}")
            return {"statusCode": 500, "body": f"Error during fetching players for league {league_id} and season {season}: {e}"}
        finally:
            session.close()            

    @staticmethod
    def current_serie_a_players_filtered_by_surname_and_team(session, args):
        try:
            team = args.get('team')
            psurname = args.get('psurname')
            print("Invoked all player by surname and team with filter", team, psurname)
        
            players_teams_query = (session.query(Player, Team, Season, PlayerStatistics)
                .join(PlayerStatistics, Player.id == PlayerStatistics.player_id)
                .join(CurrentPlayerTeam, Player.id == CurrentPlayerTeam.player_id)
                .join(Season, PlayerStatistics.season_id == Season.id)
                .join(League, Season.league_id == League.id)
                .filter(
                    League.name == "Serie A",
                    League.country_name == "Italy",
                    func.unaccent(Player.name).ilike(func.unaccent(f'%{psurname}%')),
                ))

            if team:
                players_teams_query = players_teams_query.join(Team, CurrentPlayerTeam.team_id == Team.id).filter(Team.name.ilike(f'%{team}%'))
            else:
                players_teams_query = players_teams_query.join(Team, CurrentPlayerTeam.team_id == Team.id)
            
            players = players_teams_query.all()
            
            result = []

            for player, team, season, statistics in players:
                # Cerca se il giocatore è già presente nel risultato
                existing_player = next((p for p in result if p['firstname'] == player.firstname and p['lastname'] == player.lastname), None)
                
                if not existing_player:
                    # Se non esiste, crea una nuova entry per il giocatore
                    player_entry = {
                        "name": player.name,
                        "firstname": player.firstname,
                        "lastname": player.lastname,
                        "photo": player.photo,
                        "team": team.name,
                        "team_logo": team.logo,
                        "seasons": []  # Qui inseriamo le statistiche per stagione
                    }
                    result.append(player_entry)
                else:
                    player_entry = existing_player
            
                # Aggiungi le statistiche per la stagione corrente
                season_stats = {
                    "season_year": season.year,
                    "season_current": season.current,
                    "position": statistics.position,
                    "statistics": statistics._to_dict()
                }
                
                player_entry['seasons'].append(season_stats)
            
            # Ordina le stagioni dalla più recente
            for player_entry in result:
                player_entry['seasons'].sort(key=lambda x: (not x['season_current'], -x['season_year']))

            return result
                    
        except Exception as e:
            print(f"Error during fetching Serie A players for current season: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A players for current season: {e}"}
        finally:
            session.close()


    @staticmethod
    def get_player_fixtures_stats(session, player_name, last_n_rounds=None, home_away_filter='', season=None):
      try:

        # player = aliased(Player)
        team = aliased(Team)
        opponent_team = aliased(Team)
        fixture = aliased(Fixture)
        SelectedSeason = aliased(Season)

        FPS = aliased(FixturePlayerStatistics)
        CPT = aliased(CurrentPlayerTeam)
        PS = aliased(PlayerStatistics)

        # Subquery per selezionare la stagione
        selected_season_subquery = (
          session.query(SelectedSeason)
          .filter(or_(
            SelectedSeason.year == season,
            and_(season == None, SelectedSeason.current == True)
          ))
          .limit(1)
          .subquery()
        )

        num_all_matches = session.query(func.count(fixture.id)).filter(fixture.season_id == selected_season_subquery.c.id).all()[0][0]

        player = Player.get_players_by_name(session, player_name, True)

        # Subquery per selezionare le statistiche delle partite del giocatore
        player_fixtures_subquery = (
          session.query(
            player.c.name.label('player_name'),
            player.c.id,
            player.c.firstname,
            player.c.lastname,
            func.concat(player.c.firstname, ' ', player.c.lastname).label('player_full_name'),
            fixture.event_datetime,
            selected_season_subquery.c.year.label('season'),
            team.name.label('team_name'),
            PS.position.label('ps_position'),
            case(
              (fixture.home_team_id == CPT.team_id, 'home'),
              else_='away'
            ).label('home_or_away'),
            opponent_team.name.label('opponent_team'),
            fixture.id.label('fixture_id'),
            fixture.goals_home,
            fixture.goals_away,
            fixture.league_round,
            FPS,
            func.row_number().over(
              partition_by = player.c.id,
              order_by = fixture.event_datetime.desc()
            ).label("row_number")
          )
          .join(FPS, FPS.player_id == player.c.id)
          .join(CPT, player.c.id == CPT.player_id)
          .join(fixture, FPS.fixture_id == fixture.id)
          .join(team, CPT.team_id == team.id)
          .join(PS, and_(
            PS.team_id == team.id,
            PS.player_id == FPS.player_id,
            PS.season_id == fixture.season_id
          ))
          .join(opponent_team, or_(
            and_(fixture.home_team_id == opponent_team.id, CPT.team_id != opponent_team.id),
            and_(fixture.away_team_id == opponent_team.id, CPT.team_id != opponent_team.id)
          ))

          .filter(fixture.season_id == selected_season_subquery.c.id)
          # .filter(func.unaccent(player.name).ilike(func.unaccent(f"%{player_name}%")))
          .filter(or_(
            and_(home_away_filter == 'home', fixture.home_team_id == CPT.team_id),
            and_(home_away_filter == 'away', fixture.away_team_id == CPT.team_id),
            or_(home_away_filter == '', home_away_filter == None)
          ))
          .filter(FPS.games_minutes > 0)

          .filter(or_(fixture.home_team_id == CPT.team_id, fixture.away_team_id == CPT.team_id)) # -- NOTA (1)

          # -- NOTA (1) --> FrankMaverick said:
          # -- al momento non abbiamo una tabella che contiene lo storico dei trasferimenti, 
          # -- ma solo la squadra attuale del giocatore, per cui diventa fondamentale filtrare la query solo sul team attuale, 
          # -- altrimenti si avrebbero record duplicati inerenti le due squadre (perché nessuna delle due è la squadra - attuale - del player)

          .order_by(player.c.id, fixture.event_datetime.desc())
          .subquery()
        )

        result_query = session.query(
          player_fixtures_subquery.c.player_name,
          player_fixtures_subquery.c.id.label('player_id'),
          player_fixtures_subquery.c.fixture_id,
          player_fixtures_subquery.c.firstname.label('player_firstname'),
          player_fixtures_subquery.c.lastname.label('player_lastname'),
          player_fixtures_subquery.c.player_full_name,
          player_fixtures_subquery.c.season,
          player_fixtures_subquery.c.event_datetime,
          player_fixtures_subquery.c.team_name,
          player_fixtures_subquery.c.ps_position.label('position'),
          player_fixtures_subquery.c.home_or_away,
          player_fixtures_subquery.c.opponent_team,
          player_fixtures_subquery.c.league_round,
          func.concat(player_fixtures_subquery.c.goals_home, ' - ', player_fixtures_subquery.c.goals_away).label('result'),

          case(
            (and_(
                player_fixtures_subquery.c.home_or_away == 'home',
                player_fixtures_subquery.c.goals_home > player_fixtures_subquery.c.goals_away
              ), 'W'),
            (and_(
              player_fixtures_subquery.c.home_or_away == 'away',
              player_fixtures_subquery.c.goals_away > player_fixtures_subquery.c.goals_home
            ), 'W'),
            (and_(
              player_fixtures_subquery.c.home_or_away == 'away',
              player_fixtures_subquery.c.goals_home > player_fixtures_subquery.c.goals_away
            ), 'L'),
            (and_(
              player_fixtures_subquery.c.home_or_away == 'home',
              player_fixtures_subquery.c.goals_away > player_fixtures_subquery.c.goals_home
            ), 'L'),
            else_='D'
          ),

          cast(player_fixtures_subquery.c.event_datetime, String).label('event_datetime'),
          func.coalesce(player_fixtures_subquery.c.games_substitute, False).label('games_substitute'),
          func.coalesce(player_fixtures_subquery.c.rating, 0).label('rating'),
          func.coalesce(player_fixtures_subquery.c.games_minutes, 0).label('games_minutes'),
          func.coalesce(player_fixtures_subquery.c.offsides, 0).label('offsides'),
          func.coalesce(player_fixtures_subquery.c.shots_total, 0).label('shots_total'),
          func.coalesce(player_fixtures_subquery.c.shots_on, 0).label('shots_on'),
          func.coalesce(player_fixtures_subquery.c.goals_total, 0).label('goals_total'),
          func.coalesce(player_fixtures_subquery.c.goals_conceded, 0).label('goals_conceded'),
          func.coalesce(player_fixtures_subquery.c.goals_assists, 0).label('goals_assists'),
          func.coalesce(player_fixtures_subquery.c.goals_saves, 0).label('goals_saves'),
          func.coalesce(player_fixtures_subquery.c.passes_total, 0).label('passes_total'),
          func.coalesce(player_fixtures_subquery.c.passes_key, 0).label('passes_key'),
          func.coalesce(player_fixtures_subquery.c.passes_accuracy, 0).label('passes_accuracy'),
          func.coalesce(player_fixtures_subquery.c.tackles_total, 0).label('tackles_total'),
          func.coalesce(player_fixtures_subquery.c.tackles_blocks, 0).label('tackles_blocks'),
          func.coalesce(player_fixtures_subquery.c.tackles_interceptions, 0).label('tackles_interceptions'),
          func.coalesce(player_fixtures_subquery.c.duels_total, 0).label('duels_total'),
          func.coalesce(player_fixtures_subquery.c.duels_won, 0).label('duels_won'),
          func.coalesce(player_fixtures_subquery.c.dribbles_attempts, 0).label('dribbles_attempts'),
          func.coalesce(player_fixtures_subquery.c.dribbles_success, 0).label('dribbles_success'),
          func.coalesce(player_fixtures_subquery.c.dribbles_past, 0).label('dribbles_past'),
          func.coalesce(player_fixtures_subquery.c.fouls_drawn, 0).label('fouls_drawn'),
          func.coalesce(player_fixtures_subquery.c.fouls_committed, 0).label('fouls_committed'),
          func.coalesce(player_fixtures_subquery.c.cards_yellow, 0).label('cards_yellow'),
          func.coalesce(player_fixtures_subquery.c.cards_red, 0).label('cards_red'),
          func.coalesce(player_fixtures_subquery.c.penalty_won, 0).label('penalty_won'),
          func.coalesce(player_fixtures_subquery.c.penalty_committed, 0).label('penalty_committed'),
          func.coalesce(player_fixtures_subquery.c.penalty_scored, 0).label('penalty_scored'),
          func.coalesce(player_fixtures_subquery.c.penalty_missed, 0).label('penalty_missed'),
          func.coalesce(player_fixtures_subquery.c.penalty_saved, 0).label('penalty_saved')

        ).filter(player_fixtures_subquery.c.row_number <= func.coalesce(last_n_rounds, num_all_matches))

        columns = [column['name'] for column in result_query.column_descriptions]

        player_statistic = result_query.all()

        results = []
        season_selected = ''

        for row in player_statistic:
          player_dict = {}
          for attr in columns:
            if attr:
              player_dict[attr] = getattr(row, attr)
              if attr == 'season':
                season_selected = player_dict[attr]

          results.append(player_dict)

        dict_player = {
          'player_full_name' : '',
          'player_name' : '',
          'player_firstname' : '',
          'player_lastname' : '',
          'player_id' : '',
          'team_name' : '',
          'last_fixture_id': ''
        }

        dict_to_return = {
          # 'last_n_rounds' : int(last_n_rounds) if last_n_rounds else num_all_matches,
          'today_date' : str(date.today()),
          'season_selected' : season_selected,
          'players' : []
        }

        player_map = {}
        map_played_rounds_by_player_id = {}

        for row in results:
          player_id = row['player_id']

          if not player_id in player_map:
            player_map[player_id] = {
              'stats' : []
            }

            map_played_rounds_by_player_id[player_id] = []

          only_stats_row = dict(row)
          player_from_map_id = player_map[player_id]

          for key, val in row.items():

            if key in dict_player:
              player_from_map_id[key] = val
              del only_stats_row[key]

          if only_stats_row['games_minutes'] > 0:

            if len(map_played_rounds_by_player_id[player_id]) == 0:
              # player_from_map_id['last_played_fixture_id'] = row['fixture_id']
              player_from_map_id['last_round'] = row['league_round']

            map_played_rounds_by_player_id[player_id].append(row['fixture_id'])

          player_from_map_id['played_matches_number'] = len(map_played_rounds_by_player_id[player_id])
          player_from_map_id['stats'].append(only_stats_row)

        dict_to_return['players'] = list(player_map.values())

        return [dict_to_return]

      except Exception as e:
          print(traceback.format_exc())
          print(f"Error during fetching Players by params for season={season}, player_name={player_name}, last_n_rounds={last_n_rounds}, home_or_away={home_away_filter}: {e}")
          return None
      finally:
          session.close()

    @staticmethod
    def top_players_by_team_and_role(session, args):
        """
        Estrae i migliori giocatori per squadra e ruolo in una stagione di una lega di calcio.
        
        Questo metodo esegue una query complessa per ottenere le statistiche dei giocatori
        basate su diversi parametri forniti, come il nome della squadra, il ruolo del giocatore,
        la stagione, il round specifico o gli ultimi n round da considerare. Vengono aggregati
        dati statistici come gol, assist, minuti giocati, rating medio, e altro.

        Args:
            session (Session): Oggetto della sessione SQLAlchemy.
            args (dict): Dizionario con i parametri per la query. 
                Possibili parametri:
                - 'min_rating': Valutazione media minima del giocatore (predefinita 6.1)
                - 'team': Nome della squadra (filtro opzionale)
                - 'role': Ruolo del giocatore (filtro opzionale)
                - 'season': Anno della stagione (se non fornito, si usa la stagione corrente)
                - 'last_n_rounds': Numero di ultimi round da considerare
                - 'league_round': Numero del round specifico da considerare (ha priorità su last_n_rounds)
                - 'limit': Limite del numero di risultati (predefinito 5)
        
        Returns:
            list: Lista di dizionari contenenti i dettagli dei giocatori, 
            incluse statistiche come gol totali, assist, rating medio, minuti giocati, etc.
        """        
        try:
            print("INVOKED TOP PLAYERS BY TEAM AND ROLE")

            min_rating = args.get('min_rating', 6.1)
            team = args.get("team")
            role = args.get("role")
            season = args.get("season")  # Anno della stagione
            last_n_rounds = args.get("last_n_rounds")  # Numero di ultimi round da considerare
            league_round = args.get("league_round")  # Numero del round specifico
            limit = args.get("limit", 5)  # Limite dei risultati

            print(f"PARAMS: min_rating={min_rating}, team={team}, role={role}, season={season}, "
                  f"last_n_rounds={last_n_rounds}, league_round={league_round}, limit={limit}")

            ps = aliased(PlayerStatistics)
            p = aliased(Player)
            t = aliased(Team)
            f = aliased(Fixture)
            fps = aliased(FixturePlayerStatistics)

            # Subquery per ottenere la stagione selezionata o corrente
            if not season:
                selected_season = session.query(Season.id, Season.year).filter(Season.current == True, Season.league_id == 1).limit(1).first()
            else:
                selected_season = session.query(Season.id, Season.year).filter(Season.year == season, Season.league_id == 1).limit(1).first()

            if selected_season is None:
                raise ValueError("No season found")

            # DEBUG: view subquery result
            selected_season_id, selected_season_year = selected_season
            print(f"Selected Season: {selected_season_id} {selected_season_year}")

            # Recupera il numero di round della stagione fino ad oggi
            count_matches = Fixture.how_many_matches_until_now(session, selected_season_year)
            print(f"Num. of matches until now: {count_matches}")

            # Logica per gestire `last_n_rounds` e `league_round`
            if not last_n_rounds and not league_round:
                last_n_rounds = count_matches  # Considera tutta la stagione se entrambi i parametri sono null
            elif last_n_rounds and league_round:
                last_n_rounds = None  # Ignora `last_n_rounds` se `league_round` è fornito

            # Subquery per filtrare i round in base al round specifico o agli ultimi N round
            filtered_rounds_subquery = session.query(Fixture.league_round).filter(
                Fixture.season_id == selected_season_id,
                Fixture.event_datetime <= func.now()
            )

            if league_round:
                filtered_rounds_subquery = filtered_rounds_subquery.filter(Fixture.league_round == league_round).distinct()
            else:
                filtered_rounds_subquery = filtered_rounds_subquery.order_by(
                    Fixture.league_round.desc()).distinct().limit(last_n_rounds)

            filtered_rounds_subquery = filtered_rounds_subquery.subquery()

            # DEBUG: view subquery result
            filtered_rounds = session.query(filtered_rounds_subquery).all()
            print(f"Filtered rounds: {', '.join(str(tup[0]) for tup in filtered_rounds)}")

            # Conta il numero di match / round
            count_matches = len(filtered_rounds)
            matches_minimum_presence = Player.compute_matches_minum_presence(count_matches)
            print("Matches minimum presence:", matches_minimum_presence)

            # Subquery per ottenere i giocatori che hanno giocato almeno un certo numero di partite
            filtered_players_subquery = session.query(fps.player_id).\
                join(f, f.id == fps.fixture_id).\
                join(p, p.id == fps.player_id).\
                join(t, t.id == fps.team_id).\
                join(ps, and_(fps.player_id == ps.player_id, ps.season_id == f.season_id, ps.team_id == fps.team_id)).\
                filter(
                    f.season_id == selected_season_id,
                    ps.season_id == selected_season_id,
                    f.league_round.in_(filtered_rounds_subquery),
                    func.coalesce(fps.games_minutes, 0) > 0
                ).\
                filter(
                    (t.name.ilike(f'%{team}%') if team else True),
                    (ps.position.ilike(f'%{role}%') if role else True)
                ).\
                group_by(fps.player_id).\
                having(func.count(fps.fixture_id) >= matches_minimum_presence).\
                subquery()

            # Selezione dei dati
            players_data_subquery = session.query(
                fps.player_id,
                p.name.label('player_name'),
                p.photo.label('player_photo'),
                t.name.label('team_name'),
                ps.position,
                fps.goals_total,
                fps.goals_assists,
                fps.rating,
                fps.games_minutes,
                fps.games_substitute,
                fps.offsides,
                fps.shots_total,
                fps.shots_on,
                fps.goals_conceded,
                fps.goals_saves,
                fps.passes_total,
                fps.passes_key,
                fps.passes_accuracy,
                fps.tackles_total,
                fps.tackles_blocks,
                fps.tackles_interceptions,
                fps.duels_total,
                fps.duels_won,
                fps.dribbles_attempts,
                fps.dribbles_success,
                fps.dribbles_past,
                fps.fouls_drawn,
                fps.fouls_committed,
                fps.cards_yellow,
                fps.cards_red,
                fps.penalty_won,
                fps.penalty_committed,
                fps.penalty_scored,
                fps.penalty_missed,
                fps.penalty_saved
            ).join(p, fps.player_id == p.id
            ).join(f, fps.fixture_id == f.id  
            ).join(ps, and_(fps.player_id == ps.player_id, ps.season_id == f.season_id, ps.team_id == fps.team_id)
            ).join(t, fps.team_id == t.id
            ).filter(f.season_id == selected_season_id  # Filtro per la stagione selezionata
            ).filter(f.league_round.in_(filtered_rounds_subquery)  # Filtro per round selezionati
            ).filter(p.id.in_(filtered_players_subquery)  # Filtro per giocatori selezionati
            ).subquery()       

            # Criterio di ordinamento, a seconda del ruolo, nella successiva query di aggregazione
            order_criteria = []
            if role == 'Goalkeeper':
                order_criteria = [
                    asc('goals_conceded'),
                    desc('average_rating'),
                    desc('penalty_saved'),
                    desc('goals_saves'),
                    desc('total_matches_played')
                ]
            else:
                order_criteria = [
                    desc('total_goals'),
                    desc('total_assists'),
                    desc('average_rating'),
                    desc('total_matches_played')
                ]

            # Aggregazioni sui dati selezionati
            query = session.query(
                players_data_subquery.c.player_name,
                players_data_subquery.c.player_photo,
                players_data_subquery.c.team_name,
                players_data_subquery.c.position,
                func.coalesce(func.sum(players_data_subquery.c.goals_total), 0).label('total_goals'),
                func.coalesce(func.sum(players_data_subquery.c.goals_assists), 0).label('total_assists'),
                func.coalesce(func.round(cast(func.avg(players_data_subquery.c.rating), Numeric), 2), 0).label('average_rating'),
                func.coalesce(func.sum(players_data_subquery.c.games_minutes), 0).label('total_minutes'),
                func.coalesce(func.sum(players_data_subquery.c.offsides), 0).label('total_offsides'),
                func.coalesce(func.sum(players_data_subquery.c.shots_total), 0).label('total_shots'),
                func.coalesce(func.sum(players_data_subquery.c.shots_on), 0).label('shots_on_target'),
                func.coalesce(func.sum(players_data_subquery.c.goals_conceded), 0).label('goals_conceded'),
                func.coalesce(func.sum(players_data_subquery.c.goals_saves), 0).label('goals_saves'),
                func.coalesce(func.sum(players_data_subquery.c.passes_total), 0).label('passes_total'),
                func.coalesce(func.sum(players_data_subquery.c.passes_key), 0).label('passes_key'),
                func.coalesce(func.sum(players_data_subquery.c.passes_accuracy), 0).label('passes_accuracy'),
                func.coalesce(func.sum(players_data_subquery.c.tackles_total), 0).label('tackles_total'),
                func.coalesce(func.sum(players_data_subquery.c.tackles_blocks), 0).label('tackles_blocks'),
                func.coalesce(func.sum(players_data_subquery.c.tackles_interceptions), 0).label('tackles_interceptions'),
                func.coalesce(func.sum(players_data_subquery.c.duels_total), 0).label('duels_total'),
                func.coalesce(func.sum(players_data_subquery.c.duels_won), 0).label('duels_won'),
                func.coalesce(func.sum(players_data_subquery.c.dribbles_attempts), 0).label('dribbles_attempts'),
                func.coalesce(func.sum(players_data_subquery.c.dribbles_success), 0).label('dribbles_success'),
                func.coalesce(func.sum(players_data_subquery.c.dribbles_past), 0).label('dribbles_past'),
                func.coalesce(func.sum(players_data_subquery.c.fouls_drawn), 0).label('fouls_drawn'),
                func.coalesce(func.sum(players_data_subquery.c.fouls_committed), 0).label('fouls_committed'),
                func.coalesce(func.sum(players_data_subquery.c.cards_yellow), 0).label('yellow_cards'),
                func.coalesce(func.sum(players_data_subquery.c.cards_red), 0).label('red_cards'),
                func.coalesce(func.sum(players_data_subquery.c.penalty_won), 0).label('penalty_won'),
                func.coalesce(func.sum(players_data_subquery.c.penalty_committed), 0).label('penalty_committed'),
                func.coalesce(func.sum(players_data_subquery.c.penalty_scored), 0).label('penalty_scored'),
                func.coalesce(func.sum(players_data_subquery.c.penalty_missed), 0).label('penalty_missed'),
                func.coalesce(func.sum(players_data_subquery.c.penalty_saved), 0).label('penalty_saved'),
                func.count(case((players_data_subquery.c.games_minutes > 0, players_data_subquery.c.games_minutes))).label('total_matches_played')
            ).having(
                func.avg(players_data_subquery.c.rating) >= min_rating  # Filtro su avg_rating
            ).group_by(
                players_data_subquery.c.player_name,
                players_data_subquery.c.player_photo,
                players_data_subquery.c.team_name,
                players_data_subquery.c.position
            ).order_by(
                *order_criteria
            ).limit(limit)

            top_players = query.all()

            print(f"TOP PLAYERS: {top_players}")

            result = []

            for row in top_players:
                player_dict = {
                    'player_name': row.player_name,
                    'player_photo': row.player_photo,
                    'team': row.team_name,
                    'position': row.position,
                    'total_goals': row.total_goals,
                    'total_assists': row.total_assists,
                    'average_rating': float(row.average_rating),
                    'total_minutes': row.total_minutes,
                    'total_offsides': row.total_offsides,
                    'total_shots': row.total_shots,
                    'shots_on_target': row.shots_on_target,
                    'goals_conceded': row.goals_conceded,
                    'goals_saves': row.goals_saves,
                    'passes_total': row.passes_total,
                    'passes_key': row.passes_key,
                    'passes_accuracy': row.passes_accuracy,
                    'tackles_total': row.tackles_total,
                    'tackles_blocks': row.tackles_blocks,
                    'tackles_interceptions': row.tackles_interceptions,
                    'duels_total': row.duels_total,
                    'duels_won': row.duels_won,
                    'dribbles_attempts': row.dribbles_attempts,
                    'dribbles_success': row.dribbles_success,
                    'dribbles_past': row.dribbles_past,
                    'fouls_drawn': row.fouls_drawn,
                    'fouls_committed': row.fouls_committed,
                    'yellow_cards': row.yellow_cards,
                    'red_cards': row.red_cards,
                    'penalty_won': row.penalty_won,
                    'penalty_committed': row.penalty_committed,
                    'penalty_scored': row.penalty_scored,
                    'penalty_missed': row.penalty_missed,
                    'penalty_saved': row.penalty_saved,
                    'total_matches_played': row.total_matches_played,
                    'total_season_matches': count_matches,
                    'season': selected_season_year
                }
            
                result.append(player_dict)

            return result

        except Exception as e:
            print("Error during fetching top players:", e)
            session.rollback()
            return []
        finally:
            session.close()


    @staticmethod
    def best_assist_man(session, args):
        try:
            print("INVOKED BEST ASSISTMAN")
            team = args.get("team")
            role = args.get("role")
            season = args.get("season")
            ps = aliased(PlayerStatistics)
            p = aliased(Player)
            t = aliased(Team)

            query = (session.query(
                        ps,
                        p.name.label('player_name'),
                        p.photo.label('player_photo'),
                        t.name.label('team')
                    )
                    .join(p, p.id == ps.player_id)
                    .join(t, t.id == ps.team_id)
                    .join(PlayerSeason, p.id == PlayerSeason.player_id)
                    .join(Season, PlayerSeason.season_id == Season.id)
                    .filter(
                        ps.games_lineups.isnot(None),
                        ps.rating.isnot(None),
                        ps.goals_assists.isnot(None)
                    )
                    .order_by(
                        desc(ps.goals_assists),
                        desc(ps.rating)
                    )
                    )
            # Apply season filter
            if season:
                query = query.filter(Season.id == season)
            else:
                query = query.filter(Season.current == True)

            if team:
                query = query.filter(t.name.ilike(f'%{team}%'))

            if role:
                query = query.filter(ps.position.ilike(f'%{role}%'))

            assistman = query.limit(7).all()
            print("Assistman arrived", assistman)

            result = []
            
            for ps_row in assistman:
                ps, player_name, player_photo, team_name = ps_row
                player_dict = ps._to_dict() 
                player_dict['player_name'] = player_name
                player_dict['player_photo'] = player_photo
                player_dict['team'] = team_name
                
                result.append(player_dict)

            return result

        except Exception as e:
            print(f"Error during fetching Serie A top assistman: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A top assistman: {e}"}
        finally:
            session.close()

    @staticmethod
    def get_upcoming_match_and_stats_for_players(session, args):
        """
        Retrieves upcoming match information and recent performance statistics for a list of players.

        - Gets the current season for Serie A (hardcoded league_id = 1).
        - Retrieves the next fixture involving each player's team.
        - Fetches and aggregates the last 5 match statistics for each player.
        - Fetches standings information for both the player's team and the opponent's team.

        Args:
            session: The database session for executing queries.
            args: A dictionary containing the list of players (comma-separated) under the key 'players'.

        Returns:
            A dictionary containing the player's name, team name, next fixture details, recent player stats, 
            and standings for both teams.
            If an error occurs, returns a dictionary with an error message.
        """        
        try:
            print("INVOKED UPCOMING MATCH AND STATS FOR PLAYERS")

            # get current season
            league_id = 1  # Serie A
            season = Season.get_current_season(session, league_id)
            print("Current season:", season['year'])

            players = args.get("players")

            if not players:
                return {}

            # ricavo tutte le fixture del prossimo round
            next_fixtures = Fixture.get_fixtures_by_round(session, league_id=league_id, season=season['year'], round='next')

            # Risultato complessivo per tutti i giocatori
            result = {}

            # Itera per ciascun giocatore
            for player in players.split(','):
                player = player.strip()  # Rimuove eventuali spazi prima e dopo il nome
                print("Processing player:", player)

                # Ricavo la squadra a cui appartiene
                player_team_info = (session.query(Player.id.label('player_id'), Player.name.label('player_name'), CurrentPlayerTeam.team_id)
                    .join(CurrentPlayerTeam, Player.id == CurrentPlayerTeam.player_id)
                    .filter(func.unaccent(Player.name).ilike(func.unaccent(f'%{player}%')))
                    .limit(1)  # Assicuriamoci di ottenere solo un risultato
                    .first())

                if not player_team_info:
                    print(f"No team info found for player: {player}")
                    result[player] = {"error": "Player team information not found"}
                    continue

                #print('player_team_info', player_team_info)
                player_id = player_team_info.player_id
                player_name = player_team_info.player_name
                team_id = player_team_info.team_id

                # Recupera la prossima partita per la squadra del giocatore
                next_fixture = None
                for fixture in next_fixtures:
                    # Verifica se away_team_id o home_team_id corrisponde a team_id
                    if fixture['away_team_id'] == team_id or fixture['home_team_id'] == team_id:
                        next_fixture = fixture
                        break

                if not next_fixture:
                    print(f"No upcoming fixture found for player: {player}")
                    result[player] = {"error": "No upcoming fixture found"}
                    continue

                opponent_team_id = next_fixture['away_team_id'] if next_fixture['home_team_id'] == team_id else next_fixture['home_team_id']

                player_team_detail = Team.get_team_by_id(session, team_id)
                opponent_team_detail = Team.get_team_by_id(session, opponent_team_id)

                #print("next_fixture", next_fixture)
                #print("player_team_detail", player_team_detail)
                #print("opponent_team_detail", opponent_team_detail)

                # Ricavo le stats delle ultime 5 giornate del player
                last_player_stats = Player.get_player_fixtures_stats(session, player_name, last_n_rounds=5, home_away_filter=None, season=season['year'])
                
                # Aggrega le statistiche
                aggregated_player_stats = FixturePlayerStatistics.aggregate_player_stats(last_player_stats)

                # Ricavo informazioni sulla classifica delle due squadre
                player_team_standings = Standings.get_by_ids(session, season['id'], player_team_detail['id'])
                opponent_team_standings = Standings.get_by_ids(session, season['id'], opponent_team_detail['id'])

                print(player_team_standings[0])

                # Aggiungi le informazioni al risultato
                result[player] = {
                    'player_name': player_name,
                    'player_team_name': player_team_detail['name'],
                    'next_fixture': {
                        'event_datetime': next_fixture['event_datetime'],
                        'player_team_position': 'home' if next_fixture['home_team_id'] == team_id else 'away',
                        'player_team': player_team_detail['name'],
                        'opponent_team': opponent_team_detail['name'],
                        'league_round': next_fixture['league_round'],
                        'venue_name': next_fixture['venue_name']
                    },
                    'last_5_matches_player_stats': aggregated_player_stats,
                    'player_team_standings': {
                        'team': player_team_detail['name'],
                        'rank': player_team_standings[0]['rank'],
                        'points': player_team_standings[0]['points'],
                        'form': player_team_standings[0]['form'],
                        'goals_for': player_team_standings[0]['goals_for_all'],
                        'goals_against': player_team_standings[0]['goals_against_all'],
                        'played': player_team_standings[0]['played_all'],
                        'win': player_team_standings[0]['win_all'],
                        'lose': player_team_standings[0]['lose_all'],
                        'draw': player_team_standings[0]['draw_all']
                    },
                    'opponent_team_standings': {
                        'team': opponent_team_detail['name'],
                        'rank': opponent_team_standings[0]['rank'],
                        'points': opponent_team_standings[0]['points'],
                        'form': opponent_team_standings[0]['form'],
                        'goals_for': opponent_team_standings[0]['goals_for_all'],
                        'goals_against': opponent_team_standings[0]['goals_against_all'],
                        'played': opponent_team_standings[0]['played_all'],
                        'win': opponent_team_standings[0]['win_all'],
                        'lose': opponent_team_standings[0]['lose_all'],
                        'draw': opponent_team_standings[0]['draw_all']
                    },
                }

            return result

        except Exception as e:
            print(f"Error during fetching upcoming match and stats for players: {e}")
            return {"statusCode": 500, "body": f"Error during fetching upcoming match and stats for players: {e}"}
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

    def _to_basic_info_dict(self):
        return {
            'name': self.name,
            'firstname': self.firstname,
            'lastname': self.lastname,            
            'photo': self.photo
        }
    
    @staticmethod
    def compute_matches_minum_presence(all_matches_count):
        return all_matches_count * 0.7
