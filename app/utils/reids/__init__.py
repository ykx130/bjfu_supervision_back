import redis


def get_redis_con(url):
    pool = redis.ConnectionPool.from_url(url)
    return redis.Redis(connection_pool=pool)