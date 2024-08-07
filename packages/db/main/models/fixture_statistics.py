from sqlalchemy import Column, Integer, String, ForeignKey, Float, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func, delete
from models.base import Base

class FixtureStatistics(Base):
    __tablename__ = 'fixtures_statistics'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    fixture_id = Column(Integer, ForeignKey('fixtures.id', ondelete='CASCADE'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    shots_on_goal = Column(Integer)
    shots_off_goal = Column(Integer)
    total_shots = Column(Integer)
    blocked_shots = Column(Integer)
    shots_inside_box = Column(Integer)
    shots_outside_box = Column(Integer)
    fouls = Column(Integer)
    corner_kicks = Column(Integer)
    offsides = Column(Integer)
    ball_possession = Column(Float)
    yellow_cards = Column(Integer)
    red_cards = Column(Integer)
    goalkeeper_saves = Column(Integer)
    total_passes = Column(Integer)
    passes_accurate = Column(Integer)
    expected_goals = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('fixture_id', 'team_id', name='pk_fixture_team'),
    )

    fixture = relationship('Fixture', back_populates='fixture_statistics')
    team = relationship('Team', back_populates='fixture_statistics')

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<FixtureStatistics(fixture_id={self.fixture_id}, team_id={self.team_id})>"

    @staticmethod
    def handler(session, args):
        query_type = args.get("query")

        if query_type == "delete":
            return FixtureStatistics.delete_handler(session, args)
        elif query_type == "insert":
            return FixtureStatistics.insert_handler(session, args)
        elif query_type == "update":
            return FixtureStatistics.update_handler(session, args)
        elif query_type == "upsert":
            return FixtureStatistics.upsert_handler(session, args)            
        else:
            return FixtureStatistics.get_handler(session, args)

    @staticmethod
    def insert_handler(session, args):
        try:
            if 'fixtures_statistics' in args:
                ret = FixtureStatistics.insert_if_not_exists(session, args['fixtures_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to insert FixtureStatistics"}
            else:
                return {"statusCode": 400, "body": "No fixtures_statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during insert operation: {e}"}

    @staticmethod
    def upsert_handler(session, args):
        try:
            if 'fixtures_statistics' in args:
                ret = FixtureStatistics.upsert(session, args['fixtures_statistics'])
                if ret:
                    return {"statusCode": 200, "body": ret}
                else:
                    return {"statusCode": 500, "body": "Failed to upsert FixtureStatistics"}
            else:
                return {"statusCode": 400, "body": "No fixtures_statistics provided in the payload"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during upsert operation: {e}"}            

    @staticmethod
    def update_handler(session, args):
        try:
            update_fields = args.get("update_fields", {})

            if 'fixture_id' in args and 'team_id' in args:
                fixture_id = args['fixture_id']
                team_id = args['team_id']
                ret = FixtureStatistics.update_by_ids(session, fixture_id, team_id, update_fields)
                if ret:
                    return {"statusCode": 200, "body": f"Updated fields successfully for fixture_id: {fixture_id}, team_id: {team_id}"}
                else:
                    return {"statusCode": 500, "body": f"Failed to update fields for fixture_id: {fixture_id}, team_id: {team_id}"}
            else:
                return {"statusCode": 400, "body": "fixture_id and team_id are required for update"}
        except Exception as e:
            return {"statusCode": 500, "body": f"Error during update operation: {e}"}

    @staticmethod
    def get_handler(session, args):
        if 'fixture_id' in args and 'team_id' in args:
            fixture_id = args['fixture_id']
            team_id = args['team_id']
            fixture_statistic = FixtureStatistics.get_entry(session, fixture_id, team_id)
            return {"body": fixture_statistic if fixture_statistic else "FixtureStatistics not found"}
        else:
            return {"body": FixtureStatistics.get_all(session)}

    @staticmethod
    def delete_handler(session, args):
        if 'fixture_id' in args and 'team_id' in args:
            fixture_id = args['fixture_id']
            team_id = args['team_id']
            return {"body": FixtureStatistics.delete_by_ids(session, fixture_id, team_id)}
        else:
            return {"body": FixtureStatistics.delete_all(session)}

    @staticmethod
    def get_all(session):
        try:
            fixtures_statistics = session.query(FixtureStatistics).all()
            return [f._to_dict() for f in fixtures_statistics]
        except Exception as e:
            print("Error during fixtures_statistics loading:", e)
            return []
        finally:
            session.close()

    @staticmethod
    def get_entry(session, fixture_id, team_id):
        try:
            fixture_statistic = session.query(FixtureStatistics).filter_by(fixture_id=fixture_id, team_id=team_id).one_or_none()
            return fixture_statistic._to_dict() if fixture_statistic else None
        except Exception as e:
            print(f"Error during fetching FixtureStatistics for fixture_id={fixture_id}, team_id={team_id}: {e}")
            return None
        finally:
            session.close()            

    @staticmethod
    def delete_all(session):
        try:
            session.execute(delete(FixtureStatistics))
            session.commit()
            return "All fixtures_statistics deleted"
        except Exception as e:
            print("Error while deleting fixtures_statistics:", e)
            session.rollback()
            return "Error while deleting fixtures_statistics"
        finally:
            session.close()

    @staticmethod
    def delete_by_ids(session, fixture_id, team_id):
        try:
            fixture_statistic = session.query(FixtureStatistics).filter_by(fixture_id=fixture_id, team_id=team_id).one_or_none()
            if fixture_statistic:
                session.delete(fixture_statistic)
                session.commit()
                return f"FixtureStatistics with fixture_id={fixture_id}, team_id={team_id} deleted"
            else:
                return "FixtureStatistics not found"
        except Exception as e:
            print(f"Error while deleting FixtureStatistics: {e}")
            session.rollback()
            return "Error while deleting FixtureStatistics"
        finally:
            session.close()

    @staticmethod
    def insert_if_not_exists(session, fixtures_statistics):
        try:
            inserted_records = []
            for f in fixtures_statistics:
                existing_statistic = session.query(FixtureStatistics).filter_by(
                    fixture_id=f['fixture_id'],
                    team_id=f['team_id']
                ).first()

                if existing_statistic:
                    continue  # Skip insertion if the statistic already exists

                stmt = insert(FixtureStatistics).values(
                    uuid=str(uuid.uuid4()),
                    fixture_id=f.get('fixture_id'),
                    team_id=f.get('team_id'),
                    shots_on_goal=f.get('shots_on_goal'),
                    shots_off_goal=f.get('shots_off_goal'),
                    total_shots=f.get('total_shots'),
                    blocked_shots=f.get('blocked_shots'),
                    shots_inside_box=f.get('shots_inside_box'),
                    shots_outside_box=f.get('shots_outside_box'),
                    fouls=f.get('fouls'),
                    corner_kicks=f.get('corner_kicks'),
                    offsides=f.get('offsides'),
                    ball_possession=f.get('ball_possession'),
                    yellow_cards=f.get('yellow_cards'),
                    red_cards=f.get('red_cards'),
                    goalkeeper_saves=f.get('goalkeeper_saves'),
                    total_passes=f.get('total_passes'),
                    passes_accurate=f.get('passes_accurate'),
                    expected_goals=f.get('expected_goals')
                ).on_conflict_do_nothing(index_elements=['fixture_id', 'team_id'])

                session.execute(stmt)
                inserted_records.append(f)

            session.commit()
            return inserted_records
        except Exception as e:
            print("Error during fixtures_statistics saving:", e)
            session.rollback()
            return []
        finally:
            session.close()            


    @staticmethod
    def upsert(session, fixtures_statistics):
        try:
            upserted_records = []
            for f in fixtures_statistics:

                stmt = insert(FixtureStatistics).values(
                    uuid=str(uuid.uuid4()),
                    fixture_id=f.get('fixture_id'),
                    team_id=f.get('team_id'),
                    shots_on_goal=f.get('shots_on_goal'),
                    shots_off_goal=f.get('shots_off_goal'),
                    total_shots=f.get('total_shots'),
                    blocked_shots=f.get('blocked_shots'),
                    shots_inside_box=f.get('shots_inside_box'),
                    shots_outside_box=f.get('shots_outside_box'),
                    fouls=f.get('fouls'),
                    corner_kicks=f.get('corner_kicks'),
                    offsides=f.get('offsides'),
                    ball_possession=f.get('ball_possession'),
                    yellow_cards=f.get('yellow_cards'),
                    red_cards=f.get('red_cards'),
                    goalkeeper_saves=f.get('goalkeeper_saves'),
                    total_passes=f.get('total_passes'),
                    passes_accurate=f.get('passes_accurate'),
                    expected_goals=f.get('expected_goals')
                ).on_conflict_do_update(
                    index_elements=['fixture_id', 'team_id'],
                    set_={
                        'shots_on_goal': f.get('shots_on_goal'),
                        'shots_off_goal': f.get('shots_off_goal'),
                        'total_shots': f.get('total_shots'),
                        'blocked_shots': f.get('blocked_shots'),
                        'shots_inside_box': f.get('shots_inside_box'),
                        'shots_outside_box': f.get('shots_outside_box'),
                        'fouls': f.get('fouls'),
                        'corner_kicks': f.get('corner_kicks'),
                        'offsides': f.get('offsides'),
                        'ball_possession': f.get('ball_possession'),
                        'yellow_cards': f.get('yellow_cards'),
                        'red_cards': f.get('red_cards'),
                        'goalkeeper_saves': f.get('goalkeeper_saves'),
                        'total_passes': f.get('total_passes'),
                        'passes_accurate': f.get('passes_accurate'),
                        'expected_goals': f.get('expected_goals'),
                    }
                )

                session.execute(stmt)
    
                upserted_records.append(f)
    
            session.commit()
            return upserted_records
        except Exception as e:
            print("Error during fixtures_statistics upsert:", e)
            session.rollback()
            return []
        finally:
            session.close()            


    @staticmethod
    def update_by_ids(session, fixture_id, team_id, update_fields):
        try:
            session.query(FixtureStatistics).filter_by(fixture_id=fixture_id, team_id=team_id).update(update_fields)
            session.commit()
            return True
        except Exception as e:
            print(f"Error during updating FixtureStatistics for fixture_id={fixture_id}, team_id={team_id}: {e}")
            session.rollback()
            return False
        finally:
            session.close()


    def _to_dict(self):
        return {
            'uuid': self.uuid,
            'fixture_id': self.fixture_id,
            'team_id': self.team_id,
            'shots_on_goal': self.shots_on_goal,
            'shots_off_goal': self.shots_off_goal,
            'total_shots': self.total_shots,
            'blocked_shots': self.blocked_shots,
            'shots_inside_box': self.shots_inside_box,
            'shots_outside_box': self.shots_outside_box,
            'fouls': self.fouls,
            'corner_kicks': self.corner_kicks,
            'offsides': self.offsides,
            'ball_possession': self.ball_possession,
            'yellow_cards': self.yellow_cards,
            'red_cards': self.red_cards,
            'goalkeeper_saves': self.goalkeeper_saves,
            'total_passes': self.total_passes,
            'passes_accurate': self.passes_accurate,
            'expected_goals': self.expected_goals
        }
