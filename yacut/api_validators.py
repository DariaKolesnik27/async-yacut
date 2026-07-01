import re

from .error_handlers import InvalidAPIUsage


def validate_data(data):
    """Проверяет полученные url и custom_id перед созданием объекта URLMap."""

    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    url = data.get('url')
    custom_id = data.get('custom_id')
    if not url:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if custom_id:
        if len(custom_id) > 16:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        if custom_id.lower() == 'files':
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        if not bool(re.fullmatch(r"[A-Za-z0-9]+", custom_id)):
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
    return data
