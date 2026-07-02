import re
from datetime import datetime, timezone
import uuid

from sqlalchemy.exc import IntegrityError

from . import db
from .constants import (
    MAX_ATTEMPTS,
    MAX_CUSTOM_ID,
    MAX_LINK_LENGTH,
    MAX_ORIGINAL_LENGTH,
    REGULAR
)


"""
Этот проект завершает мой учебный путь на курсе, и я хочу сказать огромное
спасибо моему ревьюеру!

Ваши комментарии всегда были точными и невероятно полезными. Каждое замечание
было не просто исправлением ошибки, а полноценным уроком: Вы показывали мне,
где прячется хрупкость кода, как избежать проблем в будущем и почему одни
решения предпочтительнее других.

Я не всегда сразу понимала, зачем нужна та или иная правка, но когда
тщательнее разбиралась в вопросе, приходила в настоящий восторг - насколько
предложенное решение действительно делает код чище и надёжнее.

Благодаря Вам я научилась видеть не только «чтобы работало», но и
«как сделать лучше».

Спасибо, что терпеливо объясняли сложные вещи и помогали расти. Я понимаю, что
нахожусь только в начале пути, но фундамент, который Вы помогли заложить, даёт
мне уверенность двигаться дальше.

Для меня было большой ценностью учиться у Вас! Спасибо! ❤️
"""


class URLMap(db.Model):
    """Модель для хранения оригинальной и короткой ссылок."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(MAX_ORIGINAL_LENGTH), unique=True, nullable=False
    )
    short = db.Column(db.String(MAX_CUSTOM_ID), unique=True, nullable=False)
    timestamp = db.Column(
        db.DateTime, index=True, default=datetime.now(timezone.utc)
    )

    @staticmethod
    def get_unique_short_id():
        """Генерирует уникальный короткий идентификатор."""

        for _ in range(MAX_ATTEMPTS):
            link = uuid.uuid4().hex[:MAX_LINK_LENGTH]
            if URLMap.query.filter_by(short=link).first() is None:
                return link
        raise RuntimeError('Не удалось сгенерировать уникальный короткий ID')

    @staticmethod
    def validate_data(data):
        """
        Проверяет полученные url и custom_id перед созданием объекта URLMap.
        """

        if not data:
            raise ValueError('Отсутствует тело запроса')
        url = data.get('url')
        custom_id = data.get('custom_id')
        if not url:
            raise ValueError('"url" является обязательным полем!')
        if custom_id:
            if len(custom_id) > MAX_CUSTOM_ID:
                raise ValueError(
                    'Указано недопустимое имя для короткой ссылки'
                )
            if custom_id.lower() == 'files':
                raise ValueError(
                    'Предложенный вариант короткой ссылки уже существует.'
                )
            if not bool(re.fullmatch(REGULAR, custom_id)):
                raise ValueError(
                    'Указано недопустимое имя для короткой ссылки'
                )
        return data

    @staticmethod
    def create_url(data):
        validated_data = URLMap.validate_data(data)
        custom_id = validated_data.get('custom_id')
        short_id = custom_id if custom_id else URLMap.get_unique_short_id()
        urlmap = URLMap(original=validated_data['url'], short=short_id)
        try:
            db.session.add(urlmap)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
        return urlmap
