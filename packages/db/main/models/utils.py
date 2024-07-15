from sqlalchemy import create_engine
from models.base import Base
from sqlalchemy.exc import SQLAlchemyError
import json

def create_tables(db_url):
    try:
        engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        print("DEBUG: Tables created")
    except SQLAlchemyError as e:
        print("ERROR: Error during tables creation: %s", e)

def drop_tables(db_url):
    try:
        engine = create_engine(db_url)
        Base.metadata.drop_all(engine)
        print("DEBUG: Tables dropped")
    except SQLAlchemyError as e:
        print("ERROR: Error during tables dropping: %s", e)

class Redis_utils():
    redis_ = None
    prefix_ = None
    REDIS_DATA_EXPIRATION_S = 86400

    def __init__(self, args):
        self.prefix_ = args.get("REDIS_PREFIX")
        print("redis prefix: " + self.prefix_)

        if self.redis_ == None:
            import redis
            self.redis_ = redis.from_url(args.get("REDIS_URL"))

    def read(self, key):
        redisReturn = None
        self.redis_.ping()

        redisKey = str(self.prefix_) + str(key)

        # self.redis_.delete(redisKey) # debug purpose

        if self.redis_.exists(redisKey):
            redisReturn = json.loads(self.redis_.get(redisKey))
            print("Read from Redis")
        return redisReturn

    def write(self, args, key, payload):
        
        if args.get("REDIS_DATA_EXPIRATION_S") != None and args.get("REDIS_DATA_EXPIRATION_S")> 0:
            self.REDIS_DATA_EXPIRATION_S = args.get("REDIS_DATA_EXPIRATION_S")
            print("set REDIS_DATA_EXPIRATION in seconds by args: " + str(self.REDIS_DATA_EXPIRATION_S))

        print("REDIS_DATA_EXPIRATION in seconds: " + str(self.REDIS_DATA_EXPIRATION_S))

        self.redis_.ping()

        redisKey = str(self.prefix_) + str(key)
        self.redis_.set(redisKey, json.dumps(payload), ex=self.REDIS_DATA_EXPIRATION_S)
        print("Wrote on Redis")