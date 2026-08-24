import time
from fastapi import Request, HTTPException, status
from app.core.redis import redis_service

async def rate_limiter(request: Request, max_requests: int = 100, window_seconds: int = 60):
    client_ip = request.client.host if request.client else "unknown"
    key = f"rate_limit:{client_ip}:{request.url.path}"
    
    if not redis_service.redis:
        return
        
    try:
        current_time = int(time.time())
        pipeline = redis_service.redis.pipeline()
        pipeline.zremrangebyscore(key, 0, current_time - window_seconds)
        pipeline.zadd(key, {str(current_time): current_time})
        pipeline.zcard(key)
        pipeline.expire(key, window_seconds)
        results = await pipeline.execute()
        
        request_count = results[2]
        if request_count > max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
    except HTTPException:
        raise
    except Exception as e:
        # Fallback gracefully if redis fails
        pass
