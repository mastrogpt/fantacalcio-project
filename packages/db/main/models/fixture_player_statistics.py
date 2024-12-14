from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func, delete
from models.base import Base
from models.league import League
from models.season import Season
from models.fixtures import Fixture

class FixturePlayerStatistics(Base):
    __tablename__ = 'fixtures_players_statistics'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    fixture_id = Column(Integer, ForeignKey('fixtures.id', ondelete='CASCADE'), nullable=False)
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=True)
    position = Column(String(50))
    rating = Column(Float)
    captain = Column(Boolean)
    games_minutes = Column(Integer)
    games_substitute = Column(Boolean)
    offsides = Column(Integer)
    shots_total = Column(Integer)
    shots_on = Column(Integer)
    goals_total = Column(Integer)
    goals_conceded = Column(Integer)
    goals_assists = Column(Integer)
    goals_saves = Column(Integer)
    passes_total = Column(Integer)
    passes_key = Column(Integer)
    passes_accuracy = Column(Integer)
    tackles_total = Column(Integer)
    tackles_blocks = Column(Integer)
    tackles_interceptions = Column(Integer)
    duels_total = Column(Integer)
    duels_won = Column(Integer)
    dribbles_attempts = Column(Integer)
    dribbles_success = Column(Integer)
    dribbles_past = Column(Integer)
    fouls_drawn = Column(Integer)
    fouls_committed = Column(Integer)
    cards_yellow = Column(Integer)
    cards_red = Column(Integer)
    penalty_won = Column(Integer)
    penalty_committed = Column(Integer)
    penalty_scored = Column(Integer)
    penalty_missed = Column(Integer)
    penalty_saved = Column(Integer)
    fbrating = Column(Float)
    fantarating = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('fixture_id', 'player_id', name='pk_fixture_player'),
    )

    fixture = relationship('Fixture', back_populates='fixture_player_statistics')
    player = relationship('Player', back_populates='fixture_player_statistics')
    team = relationship('Team', back_populates='fixture_player_statistics')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<FixturePlayerStatistics(fixture_id={self.fixture_id}, player_id={self.player_id}, team_id={self.team_id})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")

        if query_type == "delete":
            return FixturePlayerStatistics.delete_handler(session, args)
        elif query_type == "insert":
            return FixturePlayerStatistics.insert_handler(session, args)
        elif query_type == "update":
            return FixturePlayerStatistics.update_handler(session, args)
        elif query_type == "upsert":
            return FixturePlayerStatistics.upsert_handler(session, args)            
        else:
            return FixturePlayerStatistics.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'fixtures_players_statistics' in args:
                ret = FixturePlayerStatistics.insert_if_not_exists(session, args['fixtures_players_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to insert FixturePlayerStatistics"}
            else:
                return {"statusCode": 400, "body": "No fixtures_players_statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'fixtures_players_statistics' in args:
                ret = FixturePlayerStatistics.upsert(session, args['fixtures_players_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert FixturePlayerStatistics"}
            else:
                return {"statusCode": 400, "body": "No fixtures_players_statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}            

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'fixture_id' in args and 'player_id' in args:
                fixture_id = args['fixture_id']
                player_id = args['player_id']
                ret = FixturePlayerStatistics.update_by_ids(session, fixture_id, player_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for fixture_id: {fixture_id}, player_id: {player_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for fixture_id: {fixture_id}, player_id: {player_id}"}
            else:
                return {"statusCode": 400, "body": "fixture_id and player_id are required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'fixture_id' in args:
            fixture_id = args['fixture_id']
            # Se 'player_id' non esiste in args, assegnamo None a player_id
            player_id = args.get('player_id', None)

            # Chiamiamo il metodo con fixture_id e, se presente, player_id
            fpstats = FixturePlayerStatistics.get_fixture_player_statistics(session, fixture_id, player_id)
    
            return {"body": fpstats if fpstats else "FixturePlayerStatistics not found"}
        elif 'get_stats_by_round_for_fixtures_and_players' in args:
            return {"body": FixturePlayerStatistics.get_stats_by_round_for_fixtures_and_players(session, args)}
        else:
            return {"body": FixturePlayerStatistics.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'fixture_id' in args and 'player_id' in args:
            fixture_id = args['fixture_id']
            player_id = args['player_id']
            return {"body": FixturePlayerStatistics.delete_by_ids(session, fixture_id, player_id)}
        else:
            return {"body": FixturePlayerStatistics.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            fixtures_players_statistics = session.query(FixturePlayerStatistics).all()
            return [f._to_dict() for f in fixtures_players_statistics]
        except Exception as e:
            print("Error during fixtures_players_statistics loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def get_fixture_player_statistics(session, fixture_id, player_id=None):
        """
        Retrieves statistics from FixturePlayerStatistics based on fixture_id and optionally player_id.

        Args:
            session (Session): The database session to use for the query.
            fixture_id (int): The ID of the fixture to filter by.
            player_id (int, optional): The ID of the player to filter by. If None, only fixture_id is used.

        Returns:
            dict | list[dict] | None: 
                - A single statistic as a dictionary if player_id is provided and found.
                - A list of statistics as dictionaries if only fixture_id is provided.
                - None if no data is found.
        """
        try:
            query = session.query(FixturePlayerStatistics).filter_by(fixture_id=fixture_id)
            if player_id is not None:
                query = query.filter_by(player_id=player_id)

            fixture_player_statistics = query.all() if player_id is None else query.one_or_none()

            if player_id is None:
                return [fps._to_dict() for fps in fixture_player_statistics] if fixture_player_statistics else None
            else:
                return fixture_player_statistics._to_dict() if fixture_player_statistics else None
        except Exception as e:
            print(f"Error during fetching FixturePlayerStatistics for fixture_id={fixture_id}, player_id={player_id}: {e}")
            return None
        finally:
            session.close()    

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(FixturePlayerStatistics))
            session.commit()
            return "All fixtures_players_statistics deleted"
        except Exception as e:
            print("Error while deleting fixtures_players_statistics:", e)
            session.rollback()
            return "Error while deleting fixtures_players_statistics"
        finally:
            session.close()

    @staticmethod
    def delete_by_ids(session, fixture_id, player_id):
        try:
            fixture_player_statistic = session.query(FixturePlayerStatistics).filter_by(fixture_id=fixture_id, player_id=player_id).one_or_none()
            if fixture_player_statistic:
                session.delete(fixture_player_statistic)
                session.commit()
                return f"FixturePlayerStatistics with fixture_id={fixture_id}, player_id={player_id} deleted"
            else:
                return "FixturePlayerStatistics not found"
        except Exception as e:
            print(f"Error while deleting FixturePlayerStatistics: {e}")
            session.rollback()
            return "Error while deleting FixturePlayerStatistics"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, fixtures_players_statistics):
        try:
            inserted_records = []
            for f in fixtures_players_statistics:
                existing_statistic = session.query(FixturePlayerStatistics).filter_by(
                    fixture_id=f['fixture_id'],
                    player_id=f['player_id']
                ).first()

                if existing_statistic:
                    continue  # Skip insertion if the statistic already exists

                stmt = insert(FixturePlayerStatistics).values(
                    uuid=str(uuid.uuid4()),
                    fixture_id=f.get('fixture_id'),
                    player_id=f.get('player_id'),
                    team_id=f.get('team_id'),
                    position=f.get('position'),
                    rating=f.get('rating'),
                    captain=f.get('captain'),
                    games_minutes=f.get('games_minutes'),
                    games_substitute=f.get('games_substitute'),
                    offsides=f.get('offsides'),
                    shots_total=f.get('shots_total'),
                    shots_on=f.get('shots_on'),
                    goals_total=f.get('goals_total'),
                    goals_conceded=f.get('goals_conceded'),
                    goals_assists=f.get('goals_assists'),
                    goals_saves=f.get('goals_saves'),
                    passes_total=f.get('passes_total'),
                    passes_key=f.get('passes_key'),
                    passes_accuracy=f.get('passes_accuracy'),
                    tackles_total=f.get('tackles_total'),
                    tackles_blocks=f.get('tackles_blocks'),
                    tackles_interceptions=f.get('tackles_interceptions'),
                    duels_total=f.get('duels_total'),
                    duels_won=f.get('duels_won'),
                    dribbles_attempts=f.get('dribbles_attempts'),
                    dribbles_success=f.get('dribbles_success'),
                    dribbles_past=f.get('dribbles_past'),
                    fouls_drawn=f.get('fouls_drawn'),
                    fouls_committed=f.get('fouls_committed'),
                    cards_yellow=f.get('cards_yellow'),
                    cards_red=f.get('cards_red'),
                    penalty_won=f.get('penalty_won'),
                    penalty_committed=f.get('penalty_committed'),
                    penalty_scored=f.get('penalty_scored'),
                    penalty_missed=f.get('penalty_missed'),
                    penalty_saved=f.get('penalty_saved'),
                    fbrating=f.get('fbrating'),
                    fantarating=f.get('fantarating')
                ).on_conflict_do_nothing(index_elements=['fixture_id', 'player_id'])

                session.execute(stmt)
                inserted_records.append(f)

            session.commit()
            if not inserted_records:
                return {"message": "No new records inserted"}
            return inserted_records
        except Exception as e:
            print("Error during fixtures_players_statistics saving:", e)
            session.rollback()
            return []
        finally:
            session.close()            


    @staticmethod
    def upsert(session, fixtures_players_statistics):
        try:
            upserted_records = []
            for f in fixtures_players_statistics:
                # Prepara i valori per il set_ evitando i campi con valore None
                update_values = {key: value for key, value in {
                    'team_id': f.get('team_id'),
                    'position': f.get('position'),
                    'rating': f.get('rating'),
                    'captain': f.get('captain'),
                    'games_minutes': f.get('games_minutes'),
                    'games_substitute': f.get('games_substitute'),
                    'offsides': f.get('offsides'),
                    'shots_total': f.get('shots_total'),
                    'shots_on': f.get('shots_on'),
                    'goals_total': f.get('goals_total'),
                    'goals_conceded': f.get('goals_conceded'),
                    'goals_assists': f.get('goals_assists'),
                    'goals_saves': f.get('goals_saves'),
                    'passes_total': f.get('passes_total'),
                    'passes_key': f.get('passes_key'),
                    'passes_accuracy': f.get('passes_accuracy'),
                    'tackles_total': f.get('tackles_total'),
                    'tackles_blocks': f.get('tackles_blocks'),
                    'tackles_interceptions': f.get('tackles_interceptions'),
                    'duels_total': f.get('duels_total'),
                    'duels_won': f.get('duels_won'),
                    'dribbles_attempts': f.get('dribbles_attempts'),
                    'dribbles_success': f.get('dribbles_success'),
                    'dribbles_past': f.get('dribbles_past'),
                    'fouls_drawn': f.get('fouls_drawn'),
                    'fouls_committed': f.get('fouls_committed'),
                    'cards_yellow': f.get('cards_yellow'),
                    'cards_red': f.get('cards_red'),
                    'penalty_won': f.get('penalty_won'),
                    'penalty_committed': f.get('penalty_committed'),
                    'penalty_scored': f.get('penalty_scored'),
                    'penalty_missed': f.get('penalty_missed'),
                    'penalty_saved': f.get('penalty_saved'),
                    'fbrating': f.get('fbrating'),
                    'fantarating': f.get('fantarating')
                }.items() if value is not None}  # Esclude i valori None

                # Inserisce o aggiorna
                stmt = insert(FixturePlayerStatistics).values(
                    uuid=str(uuid.uuid4()),
                    fixture_id=f.get('fixture_id'),
                    player_id=f.get('player_id'),
                    team_id=f.get('team_id'),
                    position=f.get('position'),
                    rating=f.get('rating'),
                    captain=f.get('captain'),
                    games_minutes=f.get('games_minutes'),
                    games_substitute=f.get('games_substitute'),
                    offsides=f.get('offsides'),
                    shots_total=f.get('shots_total'),
                    shots_on=f.get('shots_on'),
                    goals_total=f.get('goals_total'),
                    goals_conceded=f.get('goals_conceded'),
                    goals_assists=f.get('goals_assists'),
                    goals_saves=f.get('goals_saves'),
                    passes_total=f.get('passes_total'),
                    passes_key=f.get('passes_key'),
                    passes_accuracy=f.get('passes_accuracy'),
                    tackles_total=f.get('tackles_total'),
                    tackles_blocks=f.get('tackles_blocks'),
                    tackles_interceptions=f.get('tackles_interceptions'),
                    duels_total=f.get('duels_total'),
                    duels_won=f.get('duels_won'),
                    dribbles_attempts=f.get('dribbles_attempts'),
                    dribbles_success=f.get('dribbles_success'),
                    dribbles_past=f.get('dribbles_past'),
                    fouls_drawn=f.get('fouls_drawn'),
                    fouls_committed=f.get('fouls_committed'),
                    cards_yellow=f.get('cards_yellow'),
                    cards_red=f.get('cards_red'),
                    penalty_won=f.get('penalty_won'),
                    penalty_committed=f.get('penalty_committed'),
                    penalty_scored=f.get('penalty_scored'),
                    penalty_missed=f.get('penalty_missed'),
                    penalty_saved=f.get('penalty_saved'),
                    fbrating=f.get('fbrating'),
                    fantarating=f.get('fantarating')
                ).on_conflict_do_update(
                    index_elements=['fixture_id', 'player_id'],
                    set_=update_values
                )

                # Esegui la query
                session.execute(stmt)
                upserted_records.append(f)

            # Commit finale
            session.commit()
            return upserted_records

        except Exception as e:
            print("Error during fixtures_players_statistics upsert:", e)
            session.rollback()
            return []
        finally:
            session.close()            


    @staticmethod
    def update_by_ids(session, fixture_id, player_id, update_fields):
        try:
            session.query(FixturePlayerStatistics).filter_by(fixture_id=fixture_id, player_id=player_id).update(update_fields)
            session.commit()
            return True
        except Exception as e:
            print(f"Error during updating FixturePlayerStatistics for fixture_id={fixture_id}, player_id={player_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def get_stats_by_round_for_fixtures_and_players(session, args):
        """
        This function retrieves the statistics for fixtures and players for a specific round of a given season.
        If no season or round is provided, it defaults to the current season and the most recent round.

        Parameters:
        - session: The database session used for querying.
        - args: A dictionary that may contain the following optional keys:
            - 'season' (int): The year of the season. If not provided, the current season is used.
            - 'round' (int): The round number. If not provided, the last round of the season is used.

        Returns:
        - A list of dictionaries containing fixture details, player statistics, and the result status ('W', 'L' or 'D') for each player.
        """
        print("get_stats_by_round_for_fixtures_and_players")
        try:
            # Get the Serie A league details
            league = League.get_it_serie_a_league(session)
            print("league:", league['name'])

            # Determine the season: if not provided, get the current season
            season = args.get('season')
            if season:
                season_dict = Season.get_season_by_league_and_year(session, league['id'], int(season))   
            else:
                season_dict = Season.get_current_season(session, league['id'])
            print("season:", season_dict['year'])

            # Determine the round: if not provided, get the last round
            round = args.get('round')
            if round:
                fixtures = Fixture.get_fixtures_by_round(session, league_id=league['id'], season=int(season_dict['year']), round=int(round))
            else:
                fixtures = Fixture.get_fixtures_by_round(session, league_id=league['id'], season=int(season_dict['year']), round='last')

            # List to hold the final result data
            fixture_data = []

            # Iterate over each fixture to gather data
            for fixture in fixtures:
                # Extract basic fixture details
                fixture_id = fixture['id']
                fixture_details = {
                    'home_team_id': fixture['home_team_id'],
                    'goals_home': fixture['goals_home'],
                    'away_team_id': fixture['away_team_id'],
                    'goals_away': fixture['goals_away'],
                    'league_round': fixture['league_round']
                }

                # Get player statistics for the fixture
                fp_stats = FixturePlayerStatistics.get_fixture_player_statistics(session, fixture_id=fixture_id)

                # If player statistics exist, combine them with fixture data
                if fp_stats:
                    
                    for stat in fp_stats:
                        # Calculate the result status for the player
                        result_status = None
                        if fixture_details['goals_home'] == fixture_details['goals_away']:
                            result_status = 'D' #draw
                        elif stat['team_id'] == fixture_details['home_team_id']:
                            # If the player's team is the home team
                            if fixture_details['goals_home'] > fixture_details['goals_away']:
                                result_status = 'W'
                            elif fixture_details['goals_home'] < fixture_details['goals_away']:
                                result_status = 'L'
                        elif stat['team_id'] == fixture_details['away_team_id']:
                            # If the player's team is the away team
                            if fixture_details['goals_away'] > fixture_details['goals_home']:
                                result_status = 'W'
                            elif fixture_details['goals_away'] < fixture_details['goals_home']:
                                result_status = 'L'

                        # Rimuovi il campo 'uuid' da stat, se esiste
                        stat.pop('uuid', None)

                        # Combine fixture details, player statistics, and result status
                        player_data = {
                            **fixture_details,  # Fixture details
                            **stat,  # Player statistics
                            'result_status': result_status  # Result status
                        }
                        fixture_data.append(player_data)
                else:
                    fixture_data.append(fixture_details)

            #TODO: add position from player_statistics
            
            # Return the final list of fixture and player data
            return fixture_data

        except Exception as e:
            print(f"Error in get_fixtures_and_players_statistics: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    #FIXME: Add fbrating
    def aggregate_player_stats(player_stats):
        aggregated_stats = {
            "cards_red": 0,
            "cards_yellow": 0,
            "dribbles_attempts": 0,
            "dribbles_past": 0,
            "dribbles_success": 0,
            "duels_total": 0,
            "duels_won": 0,
            "fouls_committed": 0,
            "fouls_drawn": 0,
            "games_minutes": 0,
            "goals_assists": 0,
            "goals_conceded": 0,
            "goals_saves": 0,
            "goals_total": 0,
            "offsides": 0,
            "passes_accuracy": 0,
            "passes_key": 0,
            "passes_total": 0,
            "penalty_committed": 0,
            "penalty_missed": 0,
            "penalty_saved": 0,
            "penalty_scored": 0,
            "penalty_won": 0,
            "shots_on": 0,
            "shots_total": 0,
            "tackles_blocks": 0,
            "tackles_interceptions": 0,
            "tackles_total": 0,
            "rating_sum": 0,  # Somma per calcolare la media
            "fantarating_sum": 0, # Somma per calcolare la fantamedia
            "rating_count": 0  # Numero di partite per il calcolo della media
        }
    
        for stat in player_stats:
            aggregated_stats["cards_red"] += stat["cards_red"]
            aggregated_stats["cards_yellow"] += stat["cards_yellow"]
            aggregated_stats["dribbles_attempts"] += stat["dribbles_attempts"]
            aggregated_stats["dribbles_past"] += stat["dribbles_past"]
            aggregated_stats["dribbles_success"] += stat["dribbles_success"]
            aggregated_stats["duels_total"] += stat["duels_total"]
            aggregated_stats["duels_won"] += stat["duels_won"]
            aggregated_stats["fouls_committed"] += stat["fouls_committed"]
            aggregated_stats["fouls_drawn"] += stat["fouls_drawn"]
            aggregated_stats["games_minutes"] += stat["games_minutes"]
            aggregated_stats["goals_assists"] += stat["goals_assists"]
            aggregated_stats["goals_conceded"] += stat["goals_conceded"]
            aggregated_stats["goals_saves"] += stat["goals_saves"]
            aggregated_stats["goals_total"] += stat["goals_total"]
            aggregated_stats["offsides"] += stat["offsides"]
            aggregated_stats["passes_accuracy"] += stat["passes_accuracy"]
            aggregated_stats["passes_key"] += stat["passes_key"]
            aggregated_stats["passes_total"] += stat["passes_total"]
            aggregated_stats["penalty_committed"] += stat["penalty_committed"]
            aggregated_stats["penalty_missed"] += stat["penalty_missed"]
            aggregated_stats["penalty_saved"] += stat["penalty_saved"]
            aggregated_stats["penalty_scored"] += stat["penalty_scored"]
            aggregated_stats["penalty_won"] += stat["penalty_won"]
            aggregated_stats["shots_on"] += stat["shots_on"]
            aggregated_stats["shots_total"] += stat["shots_total"]
            aggregated_stats["tackles_blocks"] += stat["tackles_blocks"]
            aggregated_stats["tackles_interceptions"] += stat["tackles_interceptions"]
            aggregated_stats["tackles_total"] += stat["tackles_total"]
            
            aggregated_stats["rating_sum"] += stat["fbrating"]
            aggregated_stats["fantarating_sum"] += stat["fantarating"]
            aggregated_stats["rating_count"] += 1
    
        # Calcola la media per il rating
        if aggregated_stats["rating_count"] > 0:
            aggregated_stats["rating_avg"] = round(aggregated_stats["rating_sum"] / aggregated_stats["rating_count"], 2)
            aggregated_stats["fantarating_avg"] = round(aggregated_stats["fantarating_sum"] / aggregated_stats["rating_count"], 2)
        else:
            aggregated_stats["rating_avg"] = None
            aggregated_stats["fantarating_avg"] = None
    
        # Rimuovi la somma del rating e il conteggio
        aggregated_stats.pop("rating_sum")
        aggregated_stats.pop("fantarating_sum")
        aggregated_stats.pop("rating_count")
    
        return aggregated_stats    


    def _to_dict(self):
        return {
            'uuid': self.uuid,
            'fixture_id': self.fixture_id,
            'player_id': self.player_id,
            'team_id': self.team_id,
            'position': self.position,
            'rating': self.rating,
            'captain': self.captain,
            'games_minutes': self.games_minutes,
            'games_substitute': self.games_substitute,
            'offsides': self.offsides,
            'shots_total': self.shots_total,
            'shots_on': self.shots_on,
            'goals_total': self.goals_total,
            'goals_conceded': self.goals_conceded,
            'goals_assists': self.goals_assists,
            'goals_saves': self.goals_saves,
            'passes_total': self.passes_total,
            'passes_key': self.passes_key,
            'passes_accuracy': self.passes_accuracy,
            'tackles_total': self.tackles_total,
            'tackles_blocks': self.tackles_blocks,
            'tackles_interceptions': self.tackles_interceptions,
            'duels_total': self.duels_total,
            'duels_won': self.duels_won,
            'dribbles_attempts': self.dribbles_attempts,
            'dribbles_success': self.dribbles_success,
            'dribbles_past': self.dribbles_past,
            'fouls_drawn': self.fouls_drawn,
            'fouls_committed': self.fouls_committed,
            'cards_yellow': self.cards_yellow,
            'cards_red': self.cards_red,
            'penalty_won': self.penalty_won,
            'penalty_committed': self.penalty_committed,
            'penalty_scored': self.penalty_scored,
            'penalty_missed': self.penalty_missed,
            'penalty_saved': self.penalty_saved,
            'fbrating': self.fbrating,
            'fantarating': self.fantarating
        }

    # Campi da restituire al frontend
    def _to_dict_frontend(self):
        return {
            'position': self.position,
            'captain': self.captain,
            'games_minutes': self.games_minutes,
            'games_substitute': self.games_substitute,
            'offsides': self.offsides,
            'shots_total': self.shots_total,
            'shots_on': self.shots_on,
            'goals_total': self.goals_total,
            'goals_conceded': self.goals_conceded,
            'goals_assists': self.goals_assists,
            'goals_saves': self.goals_saves,
            'passes_total': self.passes_total,
            'passes_key': self.passes_key,
            'passes_accuracy': self.passes_accuracy,
            'tackles_total': self.tackles_total,
            'tackles_blocks': self.tackles_blocks,
            'tackles_interceptions': self.tackles_interceptions,
            'duels_total': self.duels_total,
            'duels_won': self.duels_won,
            'dribbles_attempts': self.dribbles_attempts,
            'dribbles_success': self.dribbles_success,
            'dribbles_past': self.dribbles_past,
            'fouls_drawn': self.fouls_drawn,
            'fouls_committed': self.fouls_committed,
            'cards_yellow': self.cards_yellow,
            'cards_red': self.cards_red,
            'penalty_won': self.penalty_won,
            'penalty_committed': self.penalty_committed,
            'penalty_scored': self.penalty_scored,
            'penalty_missed': self.penalty_missed,
            'penalty_saved': self.penalty_saved,
            'fbrating': self.fbrating,
            'fantarating': self.fantarating
        }
