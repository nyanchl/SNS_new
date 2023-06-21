import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-)!$^cd%!lm-@13la*z(z=g4+%5o9&65#!dgo#40jlyi(yajkal'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'sns',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'livereload',
    'django.contrib.staticfiles',
    'app',
    'accounts',
    'rest_framework',
    'corsheaders',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "livereload.middleware.LiveReloadScript",
]

#CORS
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8080',
    'http://127.0.0.1:8000',
    'http://localhost:8000',
    'http://localhost:8080',
)

ROOT_URLCONF = 'sns.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'sns.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
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

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.AllowAny',
    # ]
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
    # JWT認証
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

SIMPLE_JWT = {
    'USER_ID_FIELD': 'uuid',
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('JWT', ),
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', )
}

"""DJSOR"""
#https://djoser.readthedocs.io/en/latest/settings.html

# DJOSER = {
#     #メールアドレスでログイン
#     'LOGIN_FIELD': 'email',

#     #アカウント本登録メール
#     'SEND_ACTIVATION_EMAIL': True,

#     #アカウント本登録完了メール
#     'SEND_CONFIRMATION_EMAIL': True,

#     #メールアドレス変更完了メール
#     'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,

#     #パスワード変更完了メール
#     'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,

#     #アカウント登録時に確認用パスワード必須
#     'USER_CREATE_PASSWORD_RETYPE': True,

#     #メールアドレス変更時に確認用メールアドレス必須
#     'SET_USERNAME_RETYPE': True,

#     #パスワード変更時に確認用パスワード必須
#     'SET_PASSWORD_RETYPE': True,

#     #アカウント本登録用URL
#     'ACTIVATION_URL': 'activate/{uid}/{token}',

#     #メールアドレスリセット完了用URL
#     'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',

#     #パスワードリセット完了用URL
#     'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',

#     # カスタムユーザー用シリアライザー
#     # https://note.crohaco.net/2018/django-rest-framework-serializer/
#     # 'SERIALIZERS': {
#     #     'user_create': 'accounts.serializers.UserSerializer',
#     #     'user': 'accounts.serializers.UserSerializer',
#     #     'current_user': 'accounts.serializers.UserSerializer',
#     # },

#     "EMAIL" : {
#         # アカウント本登録
#         'activation': 'accounts.email.ActivationEmail',

#         # アカウント本登録完了
#         'confirmation': 'accounts.email.ConfirmationEmail',

#         # パスワードリセット
#         'password_reset': 'accounts.email.PasswordResetEmail',

#         # パスワードリセット完了
#         'password_changed_confirmation': 'accounts.email.PasswordChangedConfirmationEmail',

#         # メールアドレスリセット
#         'username_reset': 'accounts.email.UsernameResetEmail',

#         # メールアドレスリセット完了
#         'username_changed_confirmation': 'accounts.email.UsernameChangedConfirmationEmail',
#     }
# }

APPEND_SLASH=False

AUTH_USER_MODEL = 'accounts.AuthUser'

LOGIN_ERROR_URL = '/accounts/login'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = 'sns:base'
LOGOUT_REDIRECT_URL = '/accounts/login/'

IMAGE_URL = '/media/'
IMAGE_ROOT = os.path.join(BASE_DIR, 'media')

# Internationalization
LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'dist/static'] 

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'hoge@hoge.com'
EMAIL_HOST_USER = 'daichi_21n1102304@nnn.ed.jp'
EMAIL_HOST_PASSWORD = 'hvwmdzffcyhqtaox'
EMAIL_USE_TLS = True

ACTIVATION_EXPIRED_DAYS = 1

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')