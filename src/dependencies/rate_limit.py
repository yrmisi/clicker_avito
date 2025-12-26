from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from redis.asyncio import Redis

from src.config import settings
from src.core import get_redis
from src.services import RateLimiter


def get_rate_limiter(r: Annotated[Redis, Depends(get_redis)]) -> RateLimiter:
    """ """
    return RateLimiter(r)


def rate_limiter_factory(
    endpoint: str,
    max_requests: int,
    window_seconds: int,
):
    async def dependency(
        request: Request,
        rate_limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
    ) -> None:

        client = request.client
        if client is None:
            return

        ip_address = request.headers.get("x-forwarded-for", client.host).split(",")[0].strip()

        exceeded = await rate_limiter.is_limited(
            ip_address,
            endpoint,
            max_requests,
            window_seconds,
        )
        if exceeded:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"You have exceeded your request limit. Please try again in {window_seconds} seconds.",
                headers={
                    "Retry-After": str(window_seconds),
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Remaining": "0",
                },
            )

    return dependency


rate_limit_short_url = rate_limiter_factory(
    "short_url",
    settings.redis_db.short_url_limit,
    settings.redis_db.short_url_window,
)
