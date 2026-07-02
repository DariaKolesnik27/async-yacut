from http import HTTPStatus

from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def add_url():
    """POST-запрос на создание объекта URLMap."""

    data = request.get_json(silent=True)
    try:
        urlmap = URLMap.create_url(data)
    except ValueError as e:
        raise InvalidAPIUsage(str(e))

    return jsonify({
        'url': urlmap.original,
        'short_link': f'{request.host_url}{urlmap.short}',
    }), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_url(short_id):
    """GET-запрос на получение оригинальной ссылки."""

    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is not None:
        return jsonify({'url': urlmap.original}), HTTPStatus.OK
    raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
