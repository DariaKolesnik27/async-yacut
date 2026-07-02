from flask import flash, redirect, render_template

from . import app
from .disk import async_upload_files_to_disk
from .forms import FilesForm, URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    """
    Представление для главной страницы: отображает форму и создает
    укороченную ссылку.

    GET: возвращает шаблон index.html с пустой формой.
    POST: валидирует форму, генерирует уникальный short_id (если не задан),
          сохраняет запись в БД и показывает результат.
    """

    form = URLMapForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        url = form.original_link.data
        try:
            urlmap = URLMap.create_url({'url': url, 'custom_id': custom_id})
            flash('Ваша новая ссылка готова:')
            return render_template('index.html', form=form, urlmap=urlmap)
        except ValueError as e:
            flash(str(e))
            return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def file_view():
    """
    Страница загрузки файлов: отображение формы и асинхронная загрузка файлов
    на Яндекс Диск.

    GET: возвращает шаблон files.html с пустой формой.
    POST: при успешной валидации запускает async_upload_files_to_disk,
          для успешно загруженных файлов создаёт записи в URLMap,
          показывает ошибки через flash.
    """

    form = FilesForm()
    if form.validate_on_submit():
        files_list = []
        files = form.files.data
        result = await async_upload_files_to_disk(files)
        errors = result.get('errors')
        uploaded_files = result.get('success')
        if uploaded_files:
            for file in uploaded_files:
                urlmap = URLMap.create_url({'url': file['url']})
                files_list.append(
                    {'filename': file['filename'], 'short_id': urlmap.short}
                )
        if errors:
            for error in errors:
                flash(
                    f'Не удалось загрузить {error["filename"]}: '
                    f'{error["error"]}'
                )
        return render_template('files.html', form=form, files_list=files_list)
    return render_template('files.html', form=form)


@app.route('/<short_id>')
def redirect_view(short_id):
    """Редирект по короткой ссылке."""

    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original)
