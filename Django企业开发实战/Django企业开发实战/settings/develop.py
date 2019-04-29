from .base import *  # NOQA    #前面这个注释起的作用是PEP 8 规范检查工具不用检查这里

DEBUG = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}