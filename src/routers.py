from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from src.database import AsyncSessionDep
from src.dependencies import rate_limit_short_url
from src.exceptions import InvalidURLError, NoLongFoundError, SlugAlreadyExistsDBError
from src.services import get_long_url, get_slug
from src.utils import SlugCountInfo

router_slug: APIRouter = APIRouter()


@router_slug.post(
    "/short_url",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(rate_limit_short_url)],
)
async def generate_slug(
    long_url: Annotated[str, Body(embed=True)],
    session: AsyncSessionDep,
) -> dict[str, str | int]:
    """ """
    for attempt in range(5):
        try:
            slug_count: SlugCountInfo = await get_slug(long_url, session)
            return {
                "link": f"http://localhost/api/{slug_count.slug}",
                "creation_count": slug_count.creation_count,
            }
        except SlugAlreadyExistsDBError:
            if attempt == 4:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to generate unique slug after 5 attempts",
                )
        except InvalidURLError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="invalid URL",
            )
    # Этот код недостижим, но успокаивает Pylance
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Unexpected error",
    )


@router_slug.get("/{slug}")
async def redirect_to_url(slug: str, session: AsyncSessionDep) -> RedirectResponse:
    """ """
    try:
        url: str = await get_long_url(slug, session)
    except NoLongFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The link does not exist")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)
