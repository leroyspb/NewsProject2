"""
Django settings for news_project project.

pGenerated by 'django-admin startproject' using Django 4.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-epl_xq(2_748q0n_=5^z+7s1i9ki^r3c_%^1djj8$#umz+d2aj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'modeltranslation',  # обязательно пишем его перед админом
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'fpages',
    'news',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',

]


SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.locale.LocaleMiddleware'
    'news.middlewares.TimezoneMiddleware',


    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',

]

ROOT_URLCONF = 'news_project.urls'

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'news_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Russian')

]

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_REDIRECT_URL = "/news"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "leroyspb"
EMAIL_HOST_PASSWORD = "yljojonbmcanjros"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

DEFAULT_FROM_EMAIL = "leroyspb@yandex.ru"

SERVER_EMAIL = "leroyspb@yandex.ru"

ADMINS = (
    ('Igor', 'leroyspb@yandex.ru'),
)

MANAGERS = (
    ('Ivan', 'leroy777@bk.ru'),
    # ('Petr', 'petr@yandex.ru'),
)

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

SITE_URL = "http://127.0.0.1:8000"

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'TIMEOUT': 60,  # добавляем стандартное время ожидания в минуту (по умолчанию это 5 минут — 300 секунд)
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'), # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
    }
}


LOGGING = {
    'version': 1,  # на текущий момент это единственно допустимое значение
    'disable_existing_loggers': False,  # контролирует работу (стандартной) схемы логирования Django
    'loggers': {
        'django': {
            'handlers': ['console_debug', 'warning_console', 'console_gen_sec_info', 'console_error_critical'],
            'propagate': True,
        },

        'django.request': {
            # Логгер, принимающий все сообщения, связанные с ошибками обработки запроса.

            'handlers': ['errors_files', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        'django.server': {
            # При попытке запуска приложения с помощью runserver, логгер регистрирует сообщения

            'handlers': ['errors_files', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },

        'django.template': {
            # Логгер, взаимодействующий с системой шаблонов Django.

            'handlers': ['errors_files'],
            'level': 'ERROR',
            'propagate': True,
        },

        'django.db.backends': {
            # Сообщения, попадающие в этот логгер, относятся к взаимодействию приложения с базой данных.
            # Ошибки в моделях, взаимодействии с ними, миграциях и т. д.

            'handlers': ['errors_files'],
            'level': 'ERROR',
            'propagate': True,
        },

        'django.security': {
            # Определяет класс логгеров, регистрирующих события нарушения безопасности.

            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },

    # средства форматирования служат для определения точного формата вывода.
    'formatters': {  # формат включает в себя время, уровень сообщения, и сами сообщения.
        'simple_format_debug': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },

        'format_warning': {  # Для сообщений WARNING и выше дополнительно добавляем pathname
            'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s',
        },

        'format_error_critical': {  # для сообщений ERROR и CRITICAL добавляем стек ошибки "exc_info"
            'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s - %(exc_info)s',
        },

        'format_general_security_info': {
            # В general.log выводим INFO и выше
            # только с указанием времени, уровня логирования, модуля, в котором возникло сообщение (module) и сообщение.
            'format': '%(asctime)s - %(levelname)s - %(module)s - %(message)s',
        },
        'mail_format': {
            'format': '%(asctime)s - %(levelname)s - %(message)s - %(pathname)s',
        }

    },


    # фильтры это дополнительный механизм перенаправления сообщений от регистраторов в обработчики, позволяющий,
    # например, отправлять ошибки только из определенного источника или согласно каким-то другим критериям,
    # которые можно определять самостоятельно.
    'filters': {
        'require_debug_false': {  # фильтр, который пропускает записи только в случае, когда DEBUG = False.
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {  # фильтр, который пропускает записи только в случае, когда DEBUG = True.
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },


    # Обработчики
    # Основная задача обработчика — перенаправить сообщение (если оно не игнорируется) в нужный ресурс.
    # Данные могут записываться в файл, отправляться по почте или другой ресурс в сети
    'handlers': {
        'console_debug': {
            'level': 'DEBUG',   # В консоль должны выводиться все сообщения уровня DEBUG и выше
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple_format_debug',
        },

        'warning_console': {
            'level': 'WARNING',  # 'WARNING' по заданию, INFO можно поставить для проверки',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'format_warning',
        },

        'console_gen_sec_info': {
            'level': 'INFO',  # В файл general.log должны выводиться сообщения уровня INFO и выше
            'filters': ['require_debug_false'],  # в файл 'general.log' отправляются — только при DEBUG = False.
            'class': 'logging.FileHandler',
            'formatter': 'format_general_security_info',
            'filename': 'log_files/general.log',
        },

        'console_error_critical': {
            'level': 'ERROR',  # 'ERROR' по заданию, INFO можно поставить для проверки,
            'filters': ['require_debug_true'],  # в консоль сообщения отправляются только при DEBUG = True
            'class': 'logging.StreamHandler',
            'formatter': 'format_error_critical',
        },

        'errors_files': {  # ERROR по заданию, INFO можно поставить для проверки,
            'level': 'ERROR',  # В файл errors.log должны выводиться сообщения только уровня ERROR и CRITICAL.
            'class': 'logging.FileHandler',
            'formatter': 'format_error_critical',
            'filename': 'log_files/errors.log',
        },

        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'format_general_security_info',
            'filename': 'log_files/security.log',
        },

        'mail_admins': {
            'level': 'ERROR',  # На почту должны отправляться сообщения уровней ERROR и выше
            'filters': ['require_debug_false'],  # на почту сообщения отправляются — только при DEBUG = False.
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail_format',  # по формату, как в errors.log, но без стека ошибок
        },
    },

}


""" Регистраторы или логгеры, образуют своеобразную иерархию.
Например, если уровень логирования регистратора определен как INFO, то в него будут попадать сообщения
уровня INFO, а также WARNING, ERROR и CRITICAL. А если регистратор определен с уровнем ERROR,
то в него попадут только сообщения ERROR и CRITICAL. Если уровень логирования сообщения «ниже» уровня логирования
регистратора, то он их будет игнорировать. Однако, если регистратор не игнорирует данное сообщение,
то оно передаётся обработчику handler."""

    
    



