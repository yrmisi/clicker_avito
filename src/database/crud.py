from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.exceptions import SlugAlreadyExistsDBError
from src.utils import SlugCountInfo

from .db_config import AsyncSessionDep
from .models import ShortURL


async def add_slug_to_db(slug: str, long_url: str, session: AsyncSessionDep) -> None:
    """ """
    short_url: ShortURL = ShortURL(slug=slug, long_url=long_url)
    session.add(short_url)
    try:
        await session.commit()
    except IntegrityError:
        raise SlugAlreadyExistsDBError


async def get_long_url_by_slug_from_db(slug: str, session: AsyncSessionDep) -> str | None:
    """ """
    # query = select(ShortURL).where(ShortURL.slug==slug)
    query = select(ShortURL).filter_by(slug=slug)
    short_url: ShortURL | None = (await session.execute(query)).scalar_one_or_none()

    if short_url:
        short_url.click_count += 1
        short_url.last_accessed_at = datetime.now(timezone.utc)
        await session.commit()
        return short_url.long_url

    return None


async def get_slug_and_count_by_long_url_from_db(
    long_url: str,
    session: AsyncSessionDep,
) -> SlugCountInfo | None:
    """ """
    query = select(ShortURL).filter_by(long_url=long_url)
    short_url: ShortURL | None = (await session.execute(query)).scalar_one_or_none()

    if short_url:
        short_url.creation_count += 1
        await session.commit()
        return SlugCountInfo(slug=short_url.slug, creation_count=short_url.creation_count)

    return None
