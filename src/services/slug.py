from src.database import AsyncSessionDep, add_slug_to_db, get_slug_and_count_by_long_url_from_db
from src.exceptions import InvalidURLError, SlugAlreadyExistsDBError
from src.utils import SlugCountInfo, generate_slug, is_valid_url


async def get_slug(url: str, session: AsyncSessionDep) -> SlugCountInfo:
    """ """
    cleaned_url = url.strip().rstrip("/")

    if not is_valid_url(cleaned_url):
        raise InvalidURLError()

    slug_count: SlugCountInfo | None = await get_slug_and_count_by_long_url_from_db(
        cleaned_url,
        session,
    )
    if slug_count:
        return slug_count

    slug: str = generate_slug()
    try:
        await add_slug_to_db(slug, cleaned_url, session)
    except SlugAlreadyExistsDBError as exc:
        raise exc
    return SlugCountInfo(slug=slug, creation_count=1)
