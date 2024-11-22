# Simple rate limit with redis

This project simulate a simple scenario in a multitenant api that needs to rate limit request per tenant.

## How it works

The project exposes a simple api to post itens: 

```shell
curl -X POST "http://localhost:8000/item" \
-H "Content-Type: application/json" \
-H "tenant_id: tenant-1" \
-d '{"name": "example_item_name", "price": 60.00, "active": true}'
```

the header `tenant_id` identifies the tenant. 

We use redis as a database for store per tenant keys, and the name of the keys following the pattern `ratelimit:${tenant-id}`

At every post request it checks if are above the per-tenant limit (currently 10 requests per minute)

## Concurrency issues

When handling intense data loads, we need to pay attention to concurrency issues.

In a traditional approach, we retrieve the key from Redis, check its value, and then update it. 
However, this approach is susceptible to race conditions.

Instead, we use a sequence of atomic operations:

1. Create the key if it doesn't exist. 
2. Always increment the key's value and then check the result against the limit.

To test this approach, there is a test class in `tests/test_multiple_requests.py`. 
It performs a total of 20 requests, with 10 of them running in parallel, and verifies that 10 requests return a 200 status 
while the remaining 10 are blocked with a 429 status.