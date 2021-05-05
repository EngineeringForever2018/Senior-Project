from backend.settings.common import *

environ.Env.read_env("backend/settings/.env.local")

SECRET_KEY = env("DJANGO_SECRET_KEY")

DEBUG = False

DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
GS_BUCKET_NAME = "avpd-media-dev"

MEDIA_ROOT = "/media"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "djangodb",
        'USER': "djangouser",
        'PASSWORD': env("POSTGRES_PASSWORD"),
        # 'HOST': env("POSTGRES_DEV"),
        # Use proxy
        'HOST': "127.0.0.1",
        # This port should be the default, but just in case I'm specifying it.
        'PORT': "5432",
    }
}
