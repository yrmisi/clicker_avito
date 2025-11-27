from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import ShortURL


async def test_generate_slug(ac: AsyncClient) -> None:
    response = await ac.post("/short_url", json={"long_url": "https://www.google.com/"})

    data: dict = response.json()
    slug: str = data["link"].split("/")[-1]

    assert response.status_code == status.HTTP_201_CREATED
    assert len(data) == 2
    assert "link" in data
    assert "http://localhost/api/" in data["link"]
    assert len(slug) == 6
    assert slug.isalnum()
    assert type(data["creation_count"]) is int
    assert data["creation_count"] == 1


# async def test_generate_slug_slug_already_exists_error(ac: AsyncClient):
#     async def mock_get_slug(long_url, session):
#         raise SlugAlreadyExistsDBError()

#     with patch("src.services.get_slug", side_effect=mock_get_slug):
#         response = await ac.post("/short_url", json={"long_url": "https://example.com"})
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     assert response.json()["detail"] == "Failed to generate slug"


# async def test_slug_already_exists_error(monkeypatch, ac: AsyncClient):
#     async def mock_get_slug(long_url, session):
#         raise SlugAlreadyExistsDBError()

#     # Заменяем get_slug на мок, выбрасывающий ошибку
#     monkeypatch.setattr("src.services.get_slug", mock_get_slug)

#     response = await ac.post("/short_url", json={"long_url": "https://example.com"})
#     assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
#     assert response.json()["detail"] == "Failed to generate slug"


async def test_invalid_url_error(ac: AsyncClient) -> None:
    response = await ac.post("/short_url", json={"long_url": "htt://www.google.com/"})

    data = response.json()
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert data["detail"] == "invalid URL"


async def test_redirect_to_url(ac: AsyncClient, session: AsyncSession) -> None:
    # short_url: ShortURL = (await session.execute(select(ShortURL))).scalar_one()
    # response = await ac.get(short_url.slug)
    long_url: str = "https://www.example.com/test1"
    slug: str = "Test12"

    short_url: ShortURL = ShortURL(slug=slug, long_url=long_url)
    session.add(short_url)
    await session.commit()

    response = await ac.get(f"/{short_url.slug}")
    assert response.status_code == status.HTTP_302_FOUND
    assert response.is_redirect
    assert response.headers.get("location") == long_url


async def test_not_long_url_found_error(ac: AsyncClient, session: AsyncSession) -> None:
    slug: str = "noslug"
    response = await ac.get(f"/{slug}")

    data = response.json()
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data["detail"] == "The link does not exist"
