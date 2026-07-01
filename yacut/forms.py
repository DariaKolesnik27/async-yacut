from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import Length, Optional


from .constants import MAX_CUSTOM_ID, MAX_ORIGINAL_LENGTH


class URLMapForm(FlaskForm):
    """Форма для создания короткой ссылки."""

    original_link = URLField(
        'Длинная ссылка',
        validators=[Length(1, MAX_ORIGINAL_LENGTH)]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Length(1, MAX_CUSTOM_ID), Optional()]
    )
    submit = SubmitField('Создать')


class FilesForm(FlaskForm):
    """Форма для загрузки файлов на Яндекс Диск."""

    files = MultipleFileField()
    submit = SubmitField('Загрузить')
