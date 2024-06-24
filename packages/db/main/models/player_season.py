from sqlalchemy import Column, Integer, String, ForeignKey, delete
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class PlayerSeason(Base):
    __tablename__ = 'players_seasons'
    
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), primary_key=True)
    season_id = Column(Integer, ForeignKey('seasons.id', ondelete='CASCADE'), primary_key=True)
    
    player = relationship('Player', back_populates='player_seasons')
    season = relationship('Season', back_populates='season_players')

    def __init__(self, player_id, season_id):
        self.player_id = player_id
        self.season_id = season_id
        
    def __repr__(self):
        return f"<PlayerSeason(player_id={self.player_id}, season_id={self.season_id}, uuid='{self.uuid}')>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return PlayerSeason.delete_handler(session, args)
        elif query_type == "insert":
            return PlayerSeason.insert_handler(session, args)         
        elif query_type == "update":
            return PlayerSeason.update_handler(session, args)
        else:
            return PlayerSeason.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'player_seasons' in args:
                ret = PlayerSeason.insert_if_not_exists(session, args['player_seasons'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to save player seasons"}
            else:
                return {"statusCode": 400, "body": "No player seasons provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}            

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'player_id' in args and 'season_id' in args:
                player_id = args['player_id']
                season_id = args['season_id']
                ret = PlayerSeason.update_by_ids(session, player_id, season_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for player_id: {player_id}, season_id: {season_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for player_id: {player_id}, season_id: {season_id}"}
            else:
                return {"statusCode": 400, "body": "player_id and season_id are required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'player_id' in args and 'season_id' in args:
            player_season = PlayerSeason.get_by_ids(session, args['player_id'], args['season_id'])
            return {"body": player_season if player_season else "PlayerSeason not found"}
        else:
            return {"body": PlayerSeason.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'player_id' in args and 'season_id' in args:
            return {"body": PlayerSeason.delete_by_ids(session, args['player_id'], args['season_id'])}
        else:
            return {"body": PlayerSeason.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            player_seasons = session.query(PlayerSeason).all()
            return [ps._to_dict() for ps in player_seasons]
        except Exception as e:
            print("Error during player seasons loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(PlayerSeason))
            session.commit()
            return "All player seasons deleted"
        except Exception as e:
            print("Error while deleting player seasons:", e)
            session.rollback()
            return "Error while deleting player seasons"
        finally:
            session.close()

    @staticmethod
    def delete_by_ids(session, player_id, season_id):
        try:
            player_season = session.query(PlayerSeason).filter_by(player_id=player_id, season_id=season_id).one_or_none()
            if player_season:
                session.delete(player_season)
                session.commit()
                return f"PlayerSeason with player_id={player_id} and season_id={season_id} deleted"
            else:
                return "PlayerSeason not found"
        except Exception as e:
            print(f"Error while deleting PlayerSeason: {e}")
            session.rollback()
            return "Error while deleting PlayerSeason"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, player_seasons):
        try:
            inserted_player_seasons = []
            for ps in player_seasons:
                stmt = insert(PlayerSeason).values(
                    player_id=ps['player_id'],
                    season_id=ps['season_id']
                ).on_conflict_do_nothing(
                    index_elements=['player_id', 'season_id']
                )
                session.execute(stmt)
                inserted_player_seasons.append(ps)

            session.commit()
            return inserted_player_seasons

        except Exception as e:
            print("Error during player seasons saving:", e)
            session.rollback()
            return False

        finally:
            session.close()

    @staticmethod
    def get_by_ids(session, player_id, season_id):
        try:
            player_season = session.query(PlayerSeason).filter_by(player_id=player_id, season_id=season_id).one_or_none()
            return player_season._to_dict() if player_season else None
        except Exception as e:
            print(f"Error during fetching PlayerSeason with player_id={player_id} and season_id={season_id}: {e}")
            return None
        finally:
            session.close()

    @staticmethod
    def update_by_ids(session, player_id, season_id, update_fields):
        try:
            player_season = session.query(PlayerSeason).filter_by(player_id=player_id, season_id=season_id).one_or_none()
            if player_season:
                for field, value in update_fields.items():
                    if hasattr(player_season, field):
                        setattr(player_season, field, value)
                    else:
                        raise AttributeError(f"Field '{field}' does not exist in PlayerSeason model")
                session.commit()
                return True
            else:
                return False
        except NoResultFound:
            print(f"PlayerSeason with player_id={player_id} and season_id={season_id} not found.")
            return False
        except AttributeError as ae:
            print(f"AttributeError during update for PlayerSeason with player_id={player_id} and season_id={season_id}: {ae}")
            session.rollback()
            return False
        except Exception as e:
            print(f"Error during update for PlayerSeason with player_id={player_id} and season_id={season_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    def _to_dict(self):
        return {
            'player_id': self.player_id,
            'season_id': self.season_id,
            'uuid': self.uuid
        }
