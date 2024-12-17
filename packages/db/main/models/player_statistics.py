from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, delete
from sqlalchemy.orm import relationship, aliased
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm.exc import NoResultFound
from models.base import Base
from models.season import Season
from models.fixtures import Fixture
from models.season import Season
from models.fixture_player_statistics import FixturePlayerStatistics
import uuid

class PlayerStatistics(Base):
    __tablename__ = 'players_statistics'
    
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), primary_key=True)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), primary_key=True)
    season_id = Column(Integer, ForeignKey('seasons.id', ondelete='CASCADE'), primary_key=True)
    position = Column(String(50))
    rating = Column(Float)
    captain = Column(Boolean)
    games_appearences = Column(Integer)
    games_lineups = Column(Integer)
    games_minutes = Column(Integer)
    games_number = Column(Integer)
    substitutes_in = Column(Integer)
    substitutes_out = Column(Integer)
    substitutes_bench = Column(Integer)
    shots_total = Column(Integer)
    shots_on = Column(Integer)
    goals_total = Column(Integer)
    goals_conceded = Column(Integer)
    goals_assists = Column(Integer)
    goals_saves = Column(Integer)
    passes_total = Column(Integer)
    passes_key = Column(Integer)
    passes_accuracy = Column(Float)
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
    cards_yellowred = Column(Integer)
    cards_red = Column(Integer)
    penalty_won = Column(Integer)
    penalty_committed = Column(Integer)
    penalty_scored = Column(Integer)
    penalty_missed = Column(Integer)
    penalty_saved = Column(Integer)
    fbrating = Column(Float)
    fantarating = Column(Float)
    
    player = relationship('Player', back_populates='player_statistics')
    team = relationship('Team', back_populates='player_statistics')
    season = relationship('Season', back_populates='player_statistics')

    def __init__(self, player_id, team_id, season_id, **kwargs):
        self.player_id = player_id
        self.team_id = team_id
        self.season_id = season_id
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def __repr__(self):
        return f"<PlayerStatistics(player_id={self.player_id}, team_id={self.team_id}, season_id={self.season_id}, uuid='{self.uuid}')>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return PlayerStatistics.delete_handler(session, args)
        elif query_type == "insert":
            return PlayerStatistics.insert_handler(session, args)         
        elif query_type == "update":
            return PlayerStatistics.update_handler(session, args)
        elif query_type == "upsert":
            return PlayerStatistics.upsert_handler(session, args)
        elif query_type == "stats":
            return PlayerStatistics.stats_handler(session, args)
        else:
            return PlayerStatistics.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'player_statistics' in args:
                ret = PlayerStatistics.insert_if_not_exists(session, args['player_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "ERROR PlayerStatistics" + ret}
            else:
                return {"statusCode": 400, "body": "No player statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'player_statistics' in args:
                ret = PlayerStatistics.upsert(session, args['player_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert player statistics"}
            else:
                return {"statusCode": 400, "body": "No player statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}


    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'player_id' in args and 'team_id' in args and 'season_id' in args:
                player_id = args['player_id']
                team_id = args['team_id']
                season_id = args['season_id']
                ret = PlayerStatistics.update_entry(session, player_id, team_id, season_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for player_id: {player_id}, team_id: {team_id}, season_id: {season_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for player_id: {player_id}, team_id: {team_id}, season_id: {season_id}"}
            else:
                return {"statusCode": 400, "body": "player_id, team_id and season_id are required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def stats_handler(session, args):
        if 'aggregate_and_save_stats' in args:
            season = args.get('season')
            league_id = args.get('league_id')
            ret = PlayerStatistics.aggregate_and_save_stats(session, season, league_id)
            season = season if season else "last"
            league_id = league_id if league_id else "Serie A"
            if ret:
                return {"statusCode": 200, "body": f"Updated stats successfully for season: {season}, league_id: {league_id}"}
            else:
                return {"statusCode": 500, "body": f"Failed to update stats for season: {season}, league_id: {league_id}"} 
        else:
            return {"statusCode": 500, "body": f"No stats args"} 

    @staticmethod
    def get_handler(session, args):
        if 'player_id' in args and 'team_id' in args and 'season_id' in args:
            player_statistic = PlayerStatistics.get_by_ids(session, args['player_id'], args['team_id'], args['season_id'])
            return {"body": player_statistic if player_statistic else "PlayerStatistics not found"}
        else:
            return {"body": PlayerStatistics.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'player_id' in args and 'team_id' in args and 'season_id' in args:
            return {"body": PlayerStatistics.delete_by_ids(session, args['player_id'], args['team_id'], args['season_id'])}
        else:
            return {"body": PlayerStatistics.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            player_statistics = session.query(PlayerStatistics).all()
            return [ps._to_dict() for ps in player_statistics]
        except Exception as e:
            print("Error during player statistics loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(PlayerStatistics))
            session.commit()
            return "All player statistics deleted"
        except Exception as e:
            print("Error while deleting player statistics:", e)
            session.rollback()
            return "Error while deleting player statistics"
        finally:
            session.close()

    @staticmethod
    def delete_by_ids(session, player_id, team_id, season_id):
        try:
            player_statistic = session.query(PlayerStatistics).filter_by(player_id=player_id, team_id=team_id, season_id=season_id).one_or_none()
            if player_statistic:
                session.delete(player_statistic)
                session.commit()
                return f"PlayerStatistics with player_id={player_id}, team_id={team_id}, season_id={season_id} deleted"
            else:
                return "PlayerStatistics not found"
        except Exception as e:
            print(f"Error while deleting PlayerStatistics: {e}")
            session.rollback()
            return "Error while deleting PlayerStatistics"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, player_statistics):
        try:
            inserted_records = []
            for ps in player_statistics:
                stmt = insert(PlayerStatistics).values(
                    player_id=ps['player_id'],
                    team_id=ps['team_id'],
                    season_id=ps['season_id'],
                    uuid=str(uuid.uuid4()),
                    position=ps.get('position'),
                    rating=ps.get('rating'),
                    captain=ps.get('captain'),
                    games_appearences=ps.get('games_appearences'),
                    games_lineups=ps.get('games_lineups'),
                    games_minutes=ps.get('games_minutes'),
                    games_number=ps.get('games_number'),
                    substitutes_in=ps.get('substitutes_in'),
                    substitutes_out=ps.get('substitutes_out'),
                    substitutes_bench=ps.get('substitutes_bench'),
                    shots_total=ps.get('shots_total'),
                    shots_on=ps.get('shots_on'),
                    goals_total=ps.get('goals_total'),
                    goals_conceded=ps.get('goals_conceded'),
                    goals_assists=ps.get('goals_assists'),
                    goals_saves=ps.get('goals_saves'),
                    passes_total=ps.get('passes_total'),
                    passes_key=ps.get('passes_key'),
                    passes_accuracy=ps.get('passes_accuracy'),
                    tackles_total=ps.get('tackles_total'),
                    tackles_blocks=ps.get('tackles_blocks'),
                    tackles_interceptions=ps.get('tackles_interceptions'),
                    duels_total=ps.get('duels_total'),
                    duels_won=ps.get('duels_won'),
                    dribbles_attempts=ps.get('dribbles_attempts'),
                    dribbles_success=ps.get('dribbles_success'),
                    dribbles_past=ps.get('dribbles_past'),
                    fouls_drawn=ps.get('fouls_drawn'),
                    fouls_committed=ps.get('fouls_committed'),
                    cards_yellow=ps.get('cards_yellow'),
                    cards_yellowred=ps.get('cards_yellowred'),
                    cards_red=ps.get('cards_red'),
                    penalty_won=ps.get('penalty_won'),
                    penalty_committed=ps.get('penalty_committed'),
                    penalty_scored=ps.get('penalty_scored'),
                    penalty_missed=ps.get('penalty_missed'),
                    penalty_saved=ps.get('penalty_saved'),
                    fbrating=ps.get('fbrating'),
                    fantarating=ps.get('fantarating')
                ).on_conflict_do_nothing(
                    index_elements=['player_id', 'team_id', 'season_id']
                )
                session.execute(stmt)
                inserted_records.append(ps)
            session.commit()
            return [ps for ps in inserted_records]
        except Exception as e:
            print("Error during player statistics saving:", e)
            session.rollback()
            return []
        finally:
            session.close()

    @staticmethod
    def upsert(session, player_statistics):
        try:
            upserted_player_statistics = []

            for ps in player_statistics:
                # Tentativo di inserimento del record
                stmt = insert(PlayerStatistics).values(
                    player_id=ps['player_id'],
                    team_id=ps['team_id'],
                    season_id=ps['season_id']
                ).on_conflict_do_nothing()

                # Esegui l'inserimento
                session.execute(stmt)

                # Recupera il record inserito o esistente
                existing_record = session.query(PlayerStatistics).filter_by(
                    player_id=ps['player_id'],
                    team_id=ps['team_id'],
                    season_id=ps['season_id']
                ).first()

                # Se il record esiste
                if existing_record:
                    for field, value in ps.items():
                        if hasattr(existing_record, field):
                            setattr(existing_record, field, value)

                    # Aggiungi il record aggiornato alla lista
                    upserted_player_statistics.append(existing_record._to_dict())

            # Commit della transazione
            session.commit()

            # Restituisci i record aggiornati
            return upserted_player_statistics

        except Exception as e:
            print("Error during player statistics upserting:", e)
            session.rollback()
            return []  # Gestione dell'errore
        finally:
            session.close()

    @staticmethod
    def get_by_ids(session, player_id: int, team_id: int, season_id: int):
        try:
            from models.player import Player
            from models.team import Team

            result = (session.query(PlayerStatistics, Player, Team)
                .join(Player, PlayerStatistics.player_id == Player.id)
                .filter(
                    PlayerStatistics.player_id == player_id,
                    PlayerStatistics.team_id == team_id,
                    PlayerStatistics.season_id == season_id,
                    Team.id == PlayerStatistics.team_id
                ).one_or_none())

            if result:

                player_statistic, player, team = result
                return {
                    'player_statistic': player_statistic._to_dict(),
                    'player': player._to_dict(),
                    'team': team._to_dict()
                }
            else:
                return None
        except Exception as e:
            print(f"Error during fetching PlayerStatistics with player_id={player_id}, team_id={team_id}, season_id={season_id}: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def update_entry(session, player_id, team_id, season_id, update_fields):
        try:
            player_statistic = session.query(PlayerStatistics).filter_by(player_id=player_id, team_id=team_id, season_id=season_id).one_or_none()
            if player_statistic:
                for field, value in update_fields.items():
                    if hasattr(player_statistic, field):
                        setattr(player_statistic, field, value)
                    else:
                        raise AttributeError(f"Field '{field}' does not exist in PlayerStatistics model")
                session.commit()
                return True
            else:
                return False
        except NoResultFound:
            print(f"PlayerStatistics with player_id={player_id}, team_id={team_id}, season_id={season_id} not found.")
            return False
        except AttributeError as ae:
            print(f"AttributeError during update for PlayerStatistics with player_id={player_id}, team_id={team_id}, season_id={season_id}: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for PlayerStatistics with player_id={player_id}, team_id={team_id}, season_id={season_id}: {e}")
            session.rollback()
            return False
        #finally:
        #    session.close()

    @staticmethod
    def aggregate_and_save_stats(session, season, league_id=None):
        try:
            if league_id is None:
                league_id = 1  # Serie A

            # Recupera la stagione per il campionato e l'anno
            season_rec = Season.get_season_by_league_and_year(session, league_id, season)
            if season_rec is None:
                season_rec = Season.get_current_season(session, league_id)

            season_id = season_rec.get('id')
            print("Season ID:", season_id)

            # Recupera l'ultimo round della stagione fino ad oggi
            last_round = Fixture.get_last_or_current_round(session, season, league_id)
            print("Last Round:", last_round)

            # Query per recuperare le statistiche dei giocatori
            player_stats_query = (
                session.query(
                    Fixture.season_id,
                    FixturePlayerStatistics
                )
                .join(Fixture, Fixture.id == FixturePlayerStatistics.fixture_id)
                .filter(
                    Fixture.league_round <= last_round,
                    Fixture.season_id == season_id,
                    FixturePlayerStatistics.games_minutes > 0
                )
            )

            player_stats_results = player_stats_query.all()

            # Raggruppa le statistiche per giocatore, stagione e squadra
            player_stats_by_player_season_team = {}
            for row in player_stats_results:
                fixture_season_id = row[0]  # Fixture.season_id
                fixture_player_stats = row[1]  # Oggetto FixturePlayerStatistics

                player_id = fixture_player_stats.player_id
                team_id = fixture_player_stats.team_id

                # Crea una chiave composta da player_id, season_id e team_id
                key = (player_id, fixture_season_id, team_id)

                if key not in player_stats_by_player_season_team:
                    player_stats_by_player_season_team[key] = []

                player_stats_by_player_season_team[key].append(fixture_player_stats)

            # Aggrega e salva le statistiche per ogni giocatore, stagione e squadra
            for (player_id, season_id, team_id), stats in player_stats_by_player_season_team.items():
                print(f"Processing aggregated stats for player_id={player_id}, season_id={season_id}, team_id={team_id}")

                if not stats:
                    print(f"No stats available for player_id={player_id}, season_id={season_id}, team_id={team_id}")
                    continue

                # Prepara i dati delle statistiche
                stats_data = [
                    {
                        key: getattr(stat, key)
                        for key in stat.__dict__.keys()
                        if not key.startswith('_') and key not in ['fixture_id', 'player_id', 'team_id', 'uuid', 'captain', 'games_substitute', 'position', 'offsides']
                    }
                    for stat in stats
                ]


                # Aggrega le statistiche del giocatore
                aggregated_stats = FixturePlayerStatistics.aggregate_player_stats(stats_data)

                # Rimuove i campi indesiderati dalle statistiche aggregate
                fields_to_remove = ['offsides']

                # Filtra le statistiche aggregate
                filtered_aggregated_stats = {key: value for key, value in aggregated_stats.items() if key not in fields_to_remove}

                # Aggiungi un controllo per i valori None
                filtered_aggregated_stats = {key: value for key, value in filtered_aggregated_stats.items() if value is not None}

                #print("Filtered Aggregated Stats:", filtered_aggregated_stats)

                # Aggiorna le stats a db
                rows_updated = session.query(PlayerStatistics).filter(
                    PlayerStatistics.player_id == player_id,
                    PlayerStatistics.team_id == team_id,
                    PlayerStatistics.season_id == season_id
                ).update(filtered_aggregated_stats, synchronize_session=False)


                if rows_updated == 0:
                    print(f"Failed to save stats for player_id={player_id}, season_id={season_id}, team_id={team_id}")
                    raise Exception(f"Failed to update statistics for player_id={player_id}, team_id={team_id}, season_id={season_id}")

                print(f"Stats for player_id={player_id}, season_id={season_id}, team_id={team_id} saved successfully")

            session.commit()
            return True

        except Exception as e:
            print("Error while aggregating and saving player statistics:", e)
            session.rollback()
            return False

        finally:
            session.close()
        

    def _to_dict(self):
        return {
            'player_id': self.player_id,
            'team_id': self.team_id,
            'season_id': self.season_id,
            'uuid': self.uuid,
            'position': self.position,
            'rating': self.rating,
            'captain': self.captain,
            'games_appearences': self.games_appearences,
            'games_lineups': self.games_lineups,
            'games_minutes': self.games_minutes,
            'games_number': self.games_number,
            'substitutes_in': self.substitutes_in,
            'substitutes_out': self.substitutes_out,
            'substitutes_bench': self.substitutes_bench,
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
            'cards_yellowred': self.cards_yellowred,
            'cards_red': self.cards_red,
            'penalty_won': self.penalty_won,
            'penalty_committed': self.penalty_committed,
            'penalty_scored': self.penalty_scored,
            'penalty_missed': self.penalty_missed,
            'penalty_saved': self.penalty_saved,
            'fbrating': self.fbrating,
            'fantarating': self.fantarating
        }
