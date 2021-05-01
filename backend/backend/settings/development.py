from backend.settings.common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u3quud34x!=4kb1qg6s419x6@(ie3f2z@8a0qb-enstzatp**7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

MEDIA_ROOT = BASE_DIR / 'media'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(BASE_DIR / 'db.sqlite3'),
    }
}
