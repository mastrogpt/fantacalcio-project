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

        if Redis_utils.redis_ is None:
            import redis
            Redis_utils.redis_ = redis.from_url(args.get("REDIS_URL"))

    @classmethod
    def _ensure_redis_initialized(cls, redis_url=None):
        if cls.redis_ is None and redis_url:
            import redis
            cls.redis_ = redis.from_url(redis_url)
            print("Redis instance initialized.")
        elif cls.redis_ is None:
            raise Exception("Redis instance is not initialized. Provide a redis_url to initialize.")

    def read(self, key):
        redisReturn = None
        self.redis_.ping()

        redisKey = str(self.prefix_) + str(key)

        redisValue = self.redis_.get(redisKey)
        ttl = self.redis_.ttl(redisKey)
        print(f"TTL for key '{redisKey}': {ttl} seconds")

        if redisValue is not None:
            redisReturn = json.loads(redisValue)
            print("Read from Redis")
        else:
            print("Redis key not found or expired: " + redisKey)

        return redisReturn

    def write(self, args, key, payload):
        expiration_time = args.get("REDIS_DATA_EXPIRATION_S", self.REDIS_DATA_EXPIRATION_S)
        
        if expiration_time > 0:
            print(f"Set REDIS_DATA_EXPIRATION in seconds by args: {expiration_time}")
        else:
            expiration_time = self.REDIS_DATA_EXPIRATION_S
            print(f"Using default REDIS_DATA_EXPIRATION in seconds: {expiration_time}")

        self.redis_.ping()

        redisKey = str(self.prefix_) + str(key)
        self.redis_.set(redisKey, json.dumps(payload), ex=expiration_time)
        print(f"Wrote on Redis with expiration: {expiration_time}")
        print("Redis key: " + redisKey)

    @classmethod
    def clear_cache(cls, redis_url=None):
        try:
            cls._ensure_redis_initialized(redis_url)
            cls.redis_.flushdb()
            print("Redis cache cleared successfully.")
            return {"statusCode": 200, "body": "Redis cache cleared successfully"}
        except Exception as e:
            print(f"Error clearing Redis cache: {e}")
            return {"statusCode": 500, "body": "Failed to clear Redis cache"}