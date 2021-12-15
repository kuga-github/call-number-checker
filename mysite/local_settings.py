import os

SECRET_KEY = 'ak*=qx%hr+ct3@9r5pyox3*y_03oqaa&+s_@4=b*s&_s+^@wqr'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True
