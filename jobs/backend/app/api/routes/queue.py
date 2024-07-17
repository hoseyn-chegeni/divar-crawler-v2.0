from fastapi import APIRouter
import redis
import json

redis_client = redis.Redis(host="redis", port=6379)
router = APIRouter()


@router.get("/queue_instances")
async def get_queue_instances():
    queue_length = redis_client.llen("jobs_queue")
    instances = [
        json.loads(redis_client.lindex("jobs_queue", i)) for i in range(queue_length)
    ]
    return {"instances_in_queue": instances}
