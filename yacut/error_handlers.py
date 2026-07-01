from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    """Кастомное исключение для ошибок API."""

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Обрабатывает кастомные ошибки API: возвращает JSON и HTTP-статус."""

    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(500)
def internal_error(error):
    """Обрабатывает ошибки сервера (500)."""

    db.session.rollback()
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(error):
    """Обрабатывает ошибки 404 «Не найдено»."""

    return render_template('404.html'), 404
