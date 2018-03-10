import redis
import pickle
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                      db=settings.REDIS_DB, password=settings.REDIS_PASSWORD)


def get_unique_key(from_num, to_num):
    return "From"+from_num+":-:"+"To"+to_num


def set_cache(key, value, ex=None):
    try:
        r.set(key, value=pickle.dumps(value), ex=ex)
    except redis.ConnectionError:
        pass


def get_cache(key, default=None):
    val = None

    try:
        val = r.get(key)
    except redis.ConnectionError:
        pass

    if val is not None:
        return pickle.loads(val)

    return default


def expire_cache(key, time):
    try:
        r.expire(key, time)
    except redis.ConnectionError:
        pass
