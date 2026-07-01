from datetime import datetime, UTC

from . import db
from .constants import MAX_CUSTOM_ID, MAX_ORIGINAL_LENGTH


class URLMap(db.Model):
    """Модель для хранения оригинальной и короткой ссылок."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(
        db.String(MAX_ORIGINAL_LENGTH), unique=True, nullable=False
    )
    short = db.Column(db.String(MAX_CUSTOM_ID), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now(UTC))
