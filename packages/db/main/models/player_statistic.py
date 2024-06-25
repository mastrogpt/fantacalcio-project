from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, delete
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class PlayerStatistic(Base):
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
        return f"<PlayerStatistic(player_id={self.player_id}, team_id={self.team_id}, season_id={self.season_id}, uuid='{self.uuid}')>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return PlayerStatistic.delete_handler(session, args)
        elif query_type == "insert":
            return PlayerStatistic.insert_handler(session, args)         
        elif query_type == "update":
            return PlayerStatistic.update_handler(session, args)
        elif query_type == "upsert":
            return PlayerStatistic.upsert_handler(session, args)
        else:
            return PlayerStatistic.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'player_statistics' in args:
                ret = PlayerStatistic.insert_if_not_exists(session, args['player_statistics'])
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
                ret = PlayerStatistic.upsert(session, args['player_statistics'])
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
                ret = PlayerStatistic.update_by_ids(session, player_id, team_id, season_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for player_id: {player_id}, team_id: {team_id}, season_id: {season_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for player_id: {player_id}, team_id: {team_id}, season_id: {season_id}"}
            else:
                return {"statusCode": 400, "body": "player_id, team_id and season_id are required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'player_id' in args and 'team_id' in args and 'season_id' in args:
            player_statistic = PlayerStatistic.get_by_ids(session, args['player_id'], args['team_id'], args['season_id'])
            return {"body": player_statistic if player_statistic else "PlayerStatistic not found"}
        else:
            return {"body": PlayerStatistic.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'player_id' in args and 'team_id' in args and 'season_id' in args:
            return {"body": PlayerStatistic.delete_by_ids(session, args['player_id'], args['team_id'], args['season_id'])}
        else:
            return {"body": PlayerStatistic.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            player_statistics = session.query(PlayerStatistic).all()
            return [ps._to_dict() for ps in player_statistics]
        except Exception as e:
            print("Error during player statistics loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(PlayerStatistic))
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
            player_statistic = session.query(PlayerStatistic).filter_by(player_id=player_id, team_id=team_id, season_id=season_id).one_or_none()
            if player_statistic:
                session.delete(player_statistic)
                session.commit()
                return f"PlayerStatistic with player_id={player_id}, team_id={team_id}, season_id={season_id} deleted"
            else:
                return "PlayerStatistic not found"
        except Exception as e:
            print(f"Error while deleting PlayerStatistic: {e}")
            session.rollback()
            return "Error while deleting PlayerStatistic"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, player_statistics):
        try:
            inserted_records = []
            for ps in player_statistics:
                stmt = insert(PlayerStatistic).values(
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
                    penalty_saved=ps.get('penalty_saved')
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
                # Try to insert the record
                stmt = insert(PlayerStatistic).values(
                    player_id=ps['player_id'],
                    team_id=ps['team_id'],
                    season_id=ps['season_id'],
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
                    penalty_saved=ps.get('penalty_saved')
                ).on_conflict_do_nothing()
    
                # Execute the insert statement
                session.execute(stmt)
    
                # Fetch the inserted or existing record
                upserted_player_statistic = session.query(PlayerStatistic).filter_by(
                    player_id=ps['player_id'],
                    team_id=ps['team_id'],
                    season_id=ps['season_id']
                ).first()
    
                # If record already exists, update its fields
                if upserted_player_statistic:
                    upserted_player_statistic.position = ps.get('position')
                    upserted_player_statistic.rating = ps.get('rating')
                    upserted_player_statistic.captain = ps.get('captain')
                    upserted_player_statistic.games_appearences = ps.get('games_appearences')
                    upserted_player_statistic.games_lineups = ps.get('games_lineups')
                    upserted_player_statistic.games_minutes = ps.get('games_minutes')
                    upserted_player_statistic.games_number = ps.get('games_number')
                    upserted_player_statistic.substitutes_in = ps.get('substitutes_in')
                    upserted_player_statistic.substitutes_out = ps.get('substitutes_out')
                    upserted_player_statistic.substitutes_bench = ps.get('substitutes_bench')
                    upserted_player_statistic.shots_total = ps.get('shots_total')
                    upserted_player_statistic.shots_on = ps.get('shots_on')
                    upserted_player_statistic.goals_total = ps.get('goals_total')
                    upserted_player_statistic.goals_conceded = ps.get('goals_conceded')
                    upserted_player_statistic.goals_assists = ps.get('goals_assists')
                    upserted_player_statistic.goals_saves = ps.get('goals_saves')
                    upserted_player_statistic.passes_total = ps.get('passes_total')
                    upserted_player_statistic.passes_key = ps.get('passes_key')
                    upserted_player_statistic.passes_accuracy = ps.get('passes_accuracy')
                    upserted_player_statistic.tackles_total = ps.get('tackles_total')
                    upserted_player_statistic.tackles_blocks = ps.get('tackles_blocks')
                    upserted_player_statistic.tackles_interceptions = ps.get('tackles_interceptions')
                    upserted_player_statistic.duels_total = ps.get('duels_total')
                    upserted_player_statistic.duels_won = ps.get('duels_won')
                    upserted_player_statistic.dribbles_attempts = ps.get('dribbles_attempts')
                    upserted_player_statistic.dribbles_success = ps.get('dribbles_success')
                    upserted_player_statistic.dribbles_past = ps.get('dribbles_past')
                    upserted_player_statistic.fouls_drawn = ps.get('fouls_drawn')
                    upserted_player_statistic.fouls_committed = ps.get('fouls_committed')
                    upserted_player_statistic.cards_yellow = ps.get('cards_yellow')
                    upserted_player_statistic.cards_yellowred = ps.get('cards_yellowred')
                    upserted_player_statistic.cards_red = ps.get('cards_red')
                    upserted_player_statistic.penalty_won = ps.get('penalty_won')
                    upserted_player_statistic.penalty_committed = ps.get('penalty_committed')
                    upserted_player_statistic.penalty_scored = ps.get('penalty_scored')
                    upserted_player_statistic.penalty_missed = ps.get('penalty_missed')
                    upserted_player_statistic.penalty_saved = ps.get('penalty_saved')
    
                    # Add the updated player statistic to the list
                    upserted_player_statistics.append(upserted_player_statistic._to_dict())
                else:
                    # If the record did not exist and was not inserted, handle as appropriate
                    pass
    
            # Commit the transaction
            session.commit()
    
            # Return the list of upserted player statistics
            return upserted_player_statistics
    
        except Exception as e:
            print("Error during player statistics upserting:", e)
            # Rollback the transaction on error
            session.rollback()
            return []  # Return an empty list or handle error as appropriate
        finally:
            # Always close the session to clean up resources
            session.close()

    @staticmethod
    def get_by_ids(session, player_id, team_id, season_id):
        try:
            player_statistic = session.query(PlayerStatistic).filter_by(player_id=player_id, team_id=team_id, season_id=season_id).one_or_none()
            return player_statistic._to_dict() if player_statistic else None
        except Exception as e:
            print(f"Error during fetching PlayerStatistic with player_id={player_id}, team_id={team_id}, season_id={season_id}: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def update_by_ids(session, player_id, team_id, season_id, update_fields):
        try:
            player_statistic = session.query(PlayerStatistic).filter_by(player_id=player_id, team_id=team_id, season_id=season_id).one_or_none()
            if player_statistic:
                for field, value in update_fields.items():
                    if hasattr(player_statistic, field):
                        setattr(player_statistic, field, value)
                    else:
                        raise AttributeError(f"Field '{field}' does not exist in PlayerStatistic model")
                session.commit()
                return True
            else:
                return False
        except NoResultFound:
            print(f"PlayerStatistic with player_id={player_id}, team_id={team_id}, season_id={season_id} not found.")
            return False
        except AttributeError as ae:
            print(f"AttributeError during update for PlayerStatistic with player_id={player_id}, team_id={team_id}, season_id={season_id}: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for PlayerStatistic with player_id={player_id}, team_id={team_id}, season_id={season_id}: {e}")
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
            'penalty_saved': self.penalty_saved
        }
