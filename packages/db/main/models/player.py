from models.fixtures import Fixture
from sqlalchemy import Column, Integer, String, Boolean, Date, insert, UniqueConstraint, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import aliased
from sqlalchemy import func
from sqlalchemy import desc
from sqlalchemy import case, func
from models.season import Season
from models.team import Team
from models.current_player_team import CurrentPlayerTeam
from models.league import League
from models.player_season import PlayerSeason
from models.team_season import TeamSeason
from models.player_statistics import PlayerStatistics
from models.base import Base
from models.utils import Redis_utils
import uuid
from datetime import datetime
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
                return {"body": Player.get_all_current_serie_a_players(session,args)}
            return {"statusCode": 500, "body": f"Value '{all_current_serie_a_players}' of all_current_serie_a_players param is not valid"} 
        elif "current_serie_a_players_filtered_by_surname_and_team" in args:
                return {"body": Player.current_serie_a_players_filtered_by_surname_and_team(session,args)}
        return {"body": Player.get_all(session,args)}
    
    @staticmethod
    def stats_handler(session, args):
        if 'assist_man' in args:
            player = Player.best_assist_man(session, args)
            return {"body": player if player else "Player not found"}
        elif 'top_players_by_team_and_role' in args:
            player = Player.top_players_by_team_and_role(session, args)
            return {"body": player if player else "Player not found"}
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
                        TeamSeason.season_id.in_(subquery),
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
            redisKey = Player.get_all_current_serie_a_players.__name__
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
    def current_serie_a_players_filtered_by_surname_and_team(session, args):
        try:
            team = args.get('team')
            psurname = args.get('psurname')
            print("Invoked all player with filter", team, psurname)
           
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
                    Season.current == True,
                    Team.name.ilike(f'%{team}%'),
                    func.unaccent(Player.name).ilike(f'%{psurname}%'),
                 )
                .all())

            result = []

            for player in players_teams:
                player_dict = player.Player._to_dict()
                player_dict['team'] = player.Team.name
                player_dict['team_logo'] = player.Team.logo
                player_dict['team_id'] = player.Team.id
                player_dict['season_id'] = player.Season.id
                player_dict['position'] = player.PlayerStatistics.position
    
                player_dict['statistics'] = player.PlayerStatistics._to_dict()
                
                result.append(player_dict)

            return result
                       
        except Exception as e:
            print(f"Error during fetching Serie A players for current season: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A players for current season: {e}"}
        finally:
            session.close()                

            
    @staticmethod
    def top_players_by_team_and_role(session, args):
        try:
            print("INVOKED TOP PLAYERS BY TEAM AND ROLE")
            min_rating = args.get('min_rating', 6.1)
        
            count_matches = Player.how_many_matches_until_now(session, args.get('season'))
            matches_minimum_presence = Player.compute_matches_minum_presence(count_matches)
            print("MINUM MATCHES IS", matches_minimum_presence)
            team = args.get("team")
            role = args.get("role")
            season = args.get("season")
            ps = aliased(PlayerStatistics)
            p = aliased(Player)
            t = aliased(Team)

            print("ROLE IS", role)

            if (role and role == "Goalkeeper"):
                return Player.best_goalkeepers(session, matches_minimum_presence, args)

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
                .filter(ps.games_appearences.isnot(None), ps.games_appearences >= matches_minimum_presence, ps.games_lineups.isnot(None), ps.rating.isnot(None), ps.rating >= min_rating)
                .order_by(desc(ps.goals_total), desc(ps.goals_assists), desc(ps.rating), desc(ps.games_lineups), ps.team_id.asc(), ps.season_id.asc()))

            # Apply season filter
            if season:
                query = query.filter(Season.id == season)
            else:
                query = query.filter(Season.current == True)

            if team:
                query = query.filter(t.name.ilike(f'%{team}%'))

            if role:
                query = query.filter(ps.position.ilike(f'%{role}%'))

            query = query.limit(5)

            top_players = query.all()

            print("TOP PLAYERS", top_players)

            if len(top_players) == 0:
                args['min_rating'] = min_rating - 0.5
                return Player.top_players_by_team_and_role(session, args)
            
            print("TOP PLAYERS ARRIVED", top_players)
            
            result = []

            for ps, player_name, player_photo, team_name in top_players:
                player_dict = ps._to_dict()
                player_dict['player_name'] = player_name
                player_dict['player_photo'] = player_photo
                player_dict['team'] = team_name
                
                result.append(player_dict)

            return result

                            
        except Exception as e:
            print(f"Error during fetching Serie A top players: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A top players: {e}"}
        finally:
            session.close()
    

    @staticmethod
    def best_goalkeepers(session, matches_minimum_presence, args):
        try:
            print("INVOKED BEST GOALKEEPERS")
            min_rating = args.get('min_rating', 6.1)
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
                        ps.games_lineups >= matches_minimum_presence,
                        ps.rating.isnot(None),
                        ps.rating >= min_rating,
                        ps.goals_saves.isnot(None),
                        ps.goals_conceded.isnot(None)
                    )
                    .order_by(
                        ps.goals_conceded.asc(),
                        desc(ps.rating),
                        desc(ps.goals_saves),
                        desc(ps.games_lineups)
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

            goleadors = query.limit(7).all()
            print("Goalkeepers arrived", goleadors)

            if len(goleadors) == 0:
                args['min_rating'] = min_rating - 0.5
                return Player.top_players_by_team_and_role(session, args)

            result = []
            for ps_row in goleadors:
                ps, player_name, player_photo, team_name = ps_row
                player_dict = ps._to_dict() 
                player_dict['player_name'] = player_name
                player_dict['player_photo'] = player_photo
                player_dict['team'] = team_name
                
                result.append(player_dict)

            return result

        except Exception as e:
            print(f"Error during fetching Serie A top goalkeepers: {e}")
            return {"statusCode": 500, "body": f"Error during fetching Serie A top players: {e}"}
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

    @staticmethod
    def how_many_matches_until_now(session, season):
        try:
            if(season is None):
                print("Cannot calculate matches number without season, setting default season to 1")
                season = 1 #TODO handle this
            matches = session.query(Fixture).filter(Fixture.season_id == season).count()
            
            print("MATCHES len", matches / 10)
            return matches / 10
          
        except Exception as e:
            print("Error while getting number of matches", e)
            session.rollback()
            return False
        finally:
            session.close()
    
    @staticmethod
    def compute_matches_minum_presence(all_matches_count):
        return all_matches_count * 0.7
