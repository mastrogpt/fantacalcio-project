from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, delete
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import insert
from models.base import Base
import uuid

class TeamStatistics(Base):
    __tablename__ = 'teams_statistics'
    
    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), primary_key=True)
    season_id = Column(Integer, ForeignKey('seasons.id', ondelete='CASCADE'), primary_key=True)
    form = Column(String)
    matches_played_home = Column(Integer)
    matches_played_away = Column(Integer)
    matches_wins_home = Column(Integer)
    matches_wins_away = Column(Integer)
    matches_draws_home = Column(Integer)
    matches_draws_away = Column(Integer)
    matches_loses_home = Column(Integer)
    matches_loses_away = Column(Integer)
    goals_for_home = Column(Integer)
    goals_for_away = Column(Integer)
    goals_against_home = Column(Integer)
    goals_against_away = Column(Integer)
    biggest_streak_wins = Column(Integer)
    biggest_streak_draws = Column(Integer)
    biggest_streak_loses = Column(Integer)
    biggest_goals_for_home = Column(Integer)
    biggest_goals_for_away = Column(Integer)
    biggest_goals_against_home = Column(Integer)
    biggest_goals_against_away = Column(Integer)
    clean_sheet_home = Column(Integer)
    clean_sheet_away = Column(Integer)
    penalty_scored = Column(Integer)
    penalty_missed = Column(Integer)
    cards_yellow = Column(Integer)
    cards_red = Column(Integer)
    
    team = relationship('Team', back_populates='team_statistics')
    season = relationship('Season', back_populates='team_statistics')

    def __init__(self, team_id, season_id, **kwargs):
        self.team_id = team_id
        self.season_id = season_id
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def __repr__(self):
        return f"<TeamStatistics(team_id={self.team_id}, season_id={self.season_id}, uuid='{self.uuid}')>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")
      
        if query_type == "delete":
            return TeamStatistics.delete_handler(session, args)
        elif query_type == "insert":
            return TeamStatistics.insert_handler(session, args)         
        elif query_type == "update":
            return TeamStatistics.update_handler(session, args)
        elif query_type == "upsert":
            return TeamStatistics.upsert_handler(session, args)
        else:
            return TeamStatistics.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'team_statistics' in args:
                ret = TeamStatistics.insert_if_not_exists(session, args['team_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "ERROR TeamStatistics" + ret}
            else:
                return {"statusCode": 400, "body": "No team statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'team_statistics' in args:
                ret = TeamStatistics.upsert(session, args['team_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert team statistics"}
            else:
                return {"statusCode": 400, "body": "No team statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'team_id' in args and 'season_id' in args:
                team_id = args['team_id']
                season_id = args['season_id']
                ret = TeamStatistics.update_by_ids(session, team_id, season_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for team_id: {team_id}, season_id: {season_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for team_id: {team_id}, season_id: {season_id}"}
            else:
                return {"statusCode": 400, "body": "team_id and season_id are required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'team_id' in args and 'season_id' in args:
            team_statistics = TeamStatistics.get_by_ids(session, args['team_id'], args['season_id'])
            return {"body": team_statistics if team_statistics else "TeamStatistics not found"}
        else:
            return {"body": TeamStatistics.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'team_id' in args and 'season_id' in args:
            return {"body": TeamStatistics.delete_by_ids(session, args['team_id'], args['season_id'])}
        else:
            return {"body": TeamStatistics.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            team_statistics = session.query(TeamStatistics).all()
            return [ts._to_dict() for ts in team_statistics]
        except Exception as e:
            print("Error during team statistics loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(TeamStatistics))
            session.commit()
            return "All team statistics deleted"
        except Exception as e:
            print("Error while deleting team statistics:", e)
            session.rollback()
            return "Error while deleting team statistics"
        finally:
            session.close()

    @staticmethod
    def delete_by_ids(session, team_id, season_id):
        try:
            team_statistics = session.query(TeamStatistics).filter_by(team_id=team_id, season_id=season_id).one_or_none()
            if team_statistics:
                session.delete(team_statistics)
                session.commit()
                return f"TeamStatistics with team_id={team_id}, season_id={season_id} deleted"
            else:
                return "TeamStatistics not found"
        except Exception as e:
            print(f"Error while deleting TeamStatistics: {e}")
            session.rollback()
            return "Error while deleting TeamStatistics"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, team_statistics):
        try:
            inserted_records = []
            for ts in team_statistics:
                stmt = insert(TeamStatistics).values(
                    team_id=ts['team_id'],
                    season_id=ts['season_id'],
                    uuid=str(uuid.uuid4()),
                    form=ts.get('form'),
                    matches_played_home=ts.get('matches_played_home'),
                    matches_played_away=ts.get('matches_played_away'),
                    matches_wins_home=ts.get('matches_wins_home'),
                    matches_wins_away=ts.get('matches_wins_away'),
                    matches_draws_home=ts.get('matches_draws_home'),
                    matches_draws_away=ts.get('matches_draws_away'),
                    matches_loses_home=ts.get('matches_loses_home'),
                    matches_loses_away=ts.get('matches_loses_away'),
                    goals_for_home=ts.get('goals_for_home'),
                    goals_for_away=ts.get('goals_for_away'),
                    goals_against_home=ts.get('goals_against_home'),
                    goals_against_away=ts.get('goals_against_away'),
                    biggest_streak_wins=ts.get('biggest_streak_wins'),
                    biggest_streak_draws=ts.get('biggest_streak_draws'),
                    biggest_streak_loses=ts.get('biggest_streak_loses'),
                    biggest_goals_for_home=ts.get('biggest_goals_for_home'),
                    biggest_goals_for_away=ts.get('biggest_goals_for_away'),
                    biggest_goals_against_home=ts.get('biggest_goals_against_home'),
                    biggest_goals_against_away=ts.get('biggest_goals_against_away'),
                    clean_sheet_home=ts.get('clean_sheet_home'),
                    clean_sheet_away=ts.get('clean_sheet_away'),
                    penalty_scored=ts.get('penalty_scored'),
                    penalty_missed=ts.get('penalty_missed'),
                    cards_yellow=ts.get('cards_yellow'),
                    cards_red=ts.get('cards_red')
                ).on_conflict_do_nothing(
                    index_elements=['team_id', 'season_id']
                )
                session.execute(stmt)
                inserted_records.append(ts)
            session.commit()
            return [ts for ts in inserted_records]
        except Exception as e:
            print("Error during team statistics saving:", e)
            session.rollback()
            return []
        finally:
            session.close()

    @staticmethod
    def upsert(session, team_statistics):
        try:
            upserted_records = []
            for ts in team_statistics:
                stmt = insert(TeamStatistics).values(
                    team_id=ts['team_id'],
                    season_id=ts['season_id'],
                    uuid=str(uuid.uuid4()),
                    form=ts.get('form'),
                    matches_played_home=ts.get('matches_played_home'),
                    matches_played_away=ts.get('matches_played_away'),
                    matches_wins_home=ts.get('matches_wins_home'),
                    matches_wins_away=ts.get('matches_wins_away'),
                    matches_draws_home=ts.get('matches_draws_home'),
                    matches_draws_away=ts.get('matches_draws_away'),
                    matches_loses_home=ts.get('matches_loses_home'),
                    matches_loses_away=ts.get('matches_loses_away'),
                    goals_for_home=ts.get('goals_for_home'),
                    goals_for_away=ts.get('goals_for_away'),
                    goals_against_home=ts.get('goals_against_home'),
                    goals_against_away=ts.get('goals_against_away'),
                    biggest_streak_wins=ts.get('biggest_streak_wins'),
                    biggest_streak_draws=ts.get('biggest_streak_draws'),
                    biggest_streak_loses=ts.get('biggest_streak_loses'),
                    biggest_goals_for_home=ts.get('biggest_goals_for_home'),
                    biggest_goals_for_away=ts.get('biggest_goals_for_away'),
                    biggest_goals_against_home=ts.get('biggest_goals_against_home'),
                    biggest_goals_against_away=ts.get('biggest_goals_against_away'),
                    clean_sheet_home=ts.get('clean_sheet_home'),
                    clean_sheet_away=ts.get('clean_sheet_away'),
                    penalty_scored=ts.get('penalty_scored'),
                    penalty_missed=ts.get('penalty_missed'),
                    cards_yellow=ts.get('cards_yellow'),
                    cards_red=ts.get('cards_red')
                ).on_conflict_do_update(
                    index_elements=['team_id', 'season_id'],
                    set_=dict(
                        form=ts.get('form'),
                        matches_played_home=ts.get('matches_played_home'),
                        matches_played_away=ts.get('matches_played_away'),
                        matches_wins_home=ts.get('matches_wins_home'),
                        matches_wins_away=ts.get('matches_wins_away'),
                        matches_draws_home=ts.get('matches_draws_home'),
                        matches_draws_away=ts.get('matches_draws_away'),
                        matches_loses_home=ts.get('matches_loses_home'),
                        matches_loses_away=ts.get('matches_loses_away'),
                        goals_for_home=ts.get('goals_for_home'),
                        goals_for_away=ts.get('goals_for_away'),
                        goals_against_home=ts.get('goals_against_home'),
                        goals_against_away=ts.get('goals_against_away'),
                        biggest_streak_wins=ts.get('biggest_streak_wins'),
                        biggest_streak_draws=ts.get('biggest_streak_draws'),
                        biggest_streak_loses=ts.get('biggest_streak_loses'),
                        biggest_goals_for_home=ts.get('biggest_goals_for_home'),
                        biggest_goals_for_away=ts.get('biggest_goals_for_away'),
                        biggest_goals_against_home=ts.get('biggest_goals_against_home'),
                        biggest_goals_against_away=ts.get('biggest_goals_against_away'),
                        clean_sheet_home=ts.get('clean_sheet_home'),
                        clean_sheet_away=ts.get('clean_sheet_away'),
                        penalty_scored=ts.get('penalty_scored'),
                        penalty_missed=ts.get('penalty_missed'),
                        cards_yellow=ts.get('cards_yellow'),
                        cards_red=ts.get('cards_red')
                    )
                )
                session.execute(stmt)
                upserted_records.append(ts)
            session.commit()
            return [ts for ts in upserted_records]
        except Exception as e:
            print("Error during team statistics upserting:", e)
            session.rollback()
            return []
        finally:
            session.close()

    @staticmethod
    def update_by_ids(session, team_id, season_id, update_fields):
        try:
            team_statistics = session.query(TeamStatistics).filter_by(team_id=team_id, season_id=season_id).one_or_none()
            if team_statistics:
                for key, value in update_fields.items():
                    setattr(team_statistics, key, value)
                session.commit()
                return f"Updated TeamStatistics for team_id={team_id}, season_id={season_id}"
            else:
                return "TeamStatistics not found"
        except Exception as e:
            print(f"Error while updating TeamStatistics: {e}")
            session.rollback()
            return "Error while updating TeamStatistics"
        finally:
            session.close()

    @staticmethod
    def get_by_ids(session, team_id, season_id):
        try:
            team_statistics = session.query(TeamStatistics).filter_by(team_id=team_id, season_id=season_id).one_or_none()
            return team_statistics._to_dict() if team_statistics else None
        except Exception as e:
            print("Error during TeamStatistics loading:", e)
            return None
        finally:
            session.close()

    def _to_dict(self):
        return {
            'uuid': self.uuid,
            'team_id': self.team_id,
            'season_id': self.season_id,
            'form': self.form,
            'matches_played_home': self.matches_played_home,
            'matches_played_away': self.matches_played_away,
            'matches_wins_home': self.matches_wins_home,
            'matches_wins_away': self.matches_wins_away,
            'matches_draws_home': self.matches_draws_home,
            'matches_draws_away': self.matches_draws_away,
            'matches_loses_home': self.matches_loses_home,
            'matches_loses_away': self.matches_loses_away,
            'goals_for_home': self.goals_for_home,
            'goals_for_away': self.goals_for_away,
            'goals_against_home': self.goals_against_home,
            'goals_against_away': self.goals_against_away,
            'biggest_streak_wins': self.biggest_streak_wins,
            'biggest_streak_draws': self.biggest_streak_draws,
            'biggest_streak_loses': self.biggest_streak_loses,
            'biggest_goals_for_home': self.biggest_goals_for_home,
            'biggest_goals_for_away': self.biggest_goals_for_away,
            'biggest_goals_against_home': self.biggest_goals_against_home,
            'biggest_goals_against_away': self.biggest_goals_against_away,
            'clean_sheet_home': self.clean_sheet_home,
            'clean_sheet_away': self.clean_sheet_away,
            'penalty_scored': self.penalty_scored,
            'penalty_missed': self.penalty_missed,
            'cards_yellow': self.cards_yellow,
            'cards_red': self.cards_red
        }
