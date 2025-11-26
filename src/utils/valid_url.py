import re

URL_REGEX = re.compile(
    r"^"
    r"(?:https?://)?"  # необязательный протокол http:// или https://
    r"(?:www\.)?"  # необязательный www.
    r"[-a-zA-Z0-9@:%._+~#=]{1,256}"  # доменное имя (до 256 символов)
    r"\.[a-zA-Z0-9()]{1,6}"  # точка и доменная зона (например .com, .рф)
    r"(?:[-a-zA-Z0-9()@:%_+.~#?&/=]*)$"  # необязательный путь, параметры, фрагмент
)


def is_valid_url(url: str) -> bool:
    return bool(URL_REGEX.fullmatch(url))
