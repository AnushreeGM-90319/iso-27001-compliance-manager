import redis

try:
    redis_client = redis.Redis(
        host='localhost',
        port=6379,
        decode_responses=True
    )

    redis_client.ping()
    print("Redis cache connected")

except Exception as e:
    print("Redis cache unavailable:", e)
    redis_client = None