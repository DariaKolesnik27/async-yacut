import uuid

from .constants import MAX_LINK_LENGTH
from .models import URLMap


def get_unique_short_id():
    """Генерирует уникальный короткий идентификатор."""

    while True:
        link = uuid.uuid4().hex[:MAX_LINK_LENGTH]
        if URLMap.query.filter_by(short=link).first() is None:
            return link
