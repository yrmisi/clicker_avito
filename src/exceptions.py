class ShortenerBaseError(Exception):
    pass


class NoLongFoundError(ShortenerBaseError):
    pass


class SlugAlreadyExistsDBError(ShortenerBaseError):
    pass


class InvalidURLError(ShortenerBaseError):
    pass
