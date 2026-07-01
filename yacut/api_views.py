from flask import jsonify, request
from sqlalchemy.exc import IntegrityError

from . import app, db
from .api_validators import validate_data
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def add_url():
    """POST-запрос на создание объекта URLMap."""

    data = request.get_json(silent=True)
    validated_data = validate_data(data)
    custom_id = validated_data.get('custom_id')
    short_id = custom_id if custom_id else get_unique_short_id()
    urlmap = URLMap(original=validated_data['url'], short=short_id)
    try:
        db.session.add(urlmap)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )

    return jsonify({
        'url': urlmap.original,
        'short_link': f'{request.host_url}{urlmap.short}',
    }), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    """GET-запрос на получение оригинальной ссылки."""

    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is not None:
        return jsonify({'url': urlmap.original}), 200
    raise InvalidAPIUsage('Указанный id не найден', 404)
