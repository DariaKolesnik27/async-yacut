import aiohttp
import asyncio
import urllib

from . import app
from .constants import DOWNLOAD_LINK_URL, REQUEST_UPLOAD_URL


AUTH_HEADERS = {
    'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'
}


async def async_upload_files_to_disk(files):
    """
    Асинхронно загружает список файлов на Яндекс Диск.
    Возвращает словарь с двумя списками:
      - 'success': файлы, успешно загруженные (с URL для скачивания)
      - 'errors': файлы, при загрузке которых произошла ошибка
    """

    results = {'success': [], 'errors': []}
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_location(session, file)
                    )
                )
            all_results = await asyncio.gather(*tasks)
        for result in all_results:
            if result['error']:
                results['errors'].append(
                    {'filename': result['filename'], 'error': result['error']}
                )
            else:
                results['success'].append(
                    {'filename': result['filename'], 'url': result['url']}
                )

    return results


async def upload_file_and_get_location(session, file):
    """Загружает один файл на Яндекс Диск через указанную aiohttp-сессию."""

    payload = {
        'path': f'app:/{file.filename}',
        'overwrite': 'True'
    }
    async with session.get(
        headers=AUTH_HEADERS,
        params=payload,
        url=REQUEST_UPLOAD_URL
    ) as response:
        data = await response.json()
        upload_url = data['href']
        if not upload_url:
            return {
                'filename': file.filename,
                'url': None,
                'error': 'Нет href в ответе'
            }
    async with session.put(data=file.read(), url=upload_url) as response:
        if response.status != 201:
            return {
                'filename': file.filename,
                'url': None, 'error':
                f'Ошибка загрузки: {response.status}'
            }
        location = response.headers['Location']
        location = urllib.parse.unquote(location)
        location = location.replace('/disk', '')
    async with session.get(
        headers=AUTH_HEADERS,
        url=DOWNLOAD_LINK_URL,
        params={'path': location}
    ) as response:
        download_link = (await response.json())['href']
    return {'filename': file.filename, 'url': download_link, 'error': None}
