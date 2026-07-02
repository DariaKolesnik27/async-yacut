# Лимиты
MAX_ATTEMPTS = 10
MAX_CUSTOM_ID = 16
MAX_LINK_LENGTH = 6
MAX_ORIGINAL_LENGTH = 256
REGULAR = r'[A-Za-z0-9]+'

# Настройки API Яндекс Диска
API_HOST = 'https://cloud-api.yandex.net/'
API_VERSION = 'v1'

# Готовые URL
DOWNLOAD_LINK_URL = f'{API_HOST}{API_VERSION}/disk/resources/download'
REQUEST_UPLOAD_URL = f'{API_HOST}{API_VERSION}/disk/resources/upload'
