from src.database import AsyncSessionDep, get_long_url_by_slug_from_db
from src.exceptions import NoLongFoundError


async def get_long_url(slug: str, session: AsyncSessionDep) -> str:
    """ """
    long_url: str | None = await get_long_url_by_slug_from_db(slug, session)
    if long_url is None:
        raise NoLongFoundError()
    return long_url
