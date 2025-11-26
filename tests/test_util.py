from utils import generate_slug, SlugCountInfo, is_valid_url


def test_generate_slug() -> None:
    """ """
    slug = generate_slug()
    assert type(slug) is str
    assert len(slug) == 6
    assert slug.isalnum()


def test_slug_count_info() -> None:
    """ """
    slug = generate_slug()
    slug_count = SlugCountInfo(slug, 1)

    assert type(slug_count) is SlugCountInfo
    assert slug_count.slug == slug
    assert slug_count.creation_count == 1


def test_is_valid_url() -> None:
    """  """
    url = "https://www.example.com/test"

    assert is_valid_url(url)


def test_negative_is_valid_url() -> None:
    """ """
    url = "hps://www.example.com/test"

    assert is_valid_url(url) is False
