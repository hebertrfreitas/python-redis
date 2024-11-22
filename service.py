import redis

from models import Item
from typing import List
from redis import Redis
from fastapi import HTTPException

items: List[Item] = []


def redis_client():
    return Redis(host='localhost', port='6379', db='0')


def create_item(item: Item, tenant_id: str):
    """
    Create and item checking the rate limit.
    If the tenant_id submit more the 10 request in a minute then reject the request with 429.

    Instead of get the key from redis, check the value and then update it, we use a sequence of atomic operations
    to prevent concurrency issues:

    1. create the key if it doesn't exist
    2. always increment the value of the key and with the result we check the limit.

    :param item:
    :param tenant_id:
    :return:
    """

    r = redis_client()
    ratelimit_key = f'ratelimit:{tenant_id}'

    r.set(name=ratelimit_key, nx=True, ex=60, value=0)
    ratelimit_value = r.incr(ratelimit_key)
    print(f'ratelimit_value: {ratelimit_value}')
    if int(ratelimit_value) > 10:
        print("rate limit exceeded")
        raise HTTPException(status_code=429, detail='rate limit exceeded')

    items.append(item)
    print('item added')
