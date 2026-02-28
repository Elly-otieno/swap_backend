from pathlib import Path
import os
import tempfile
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# DIDIT
DIDIT_API_KEY = os.getenv("DIDIT_API_KEY")
DIDIT_BASE_URL = "https://api.didit.me"
DIDIT_WEBHOOK_SECRET = os.getenv("DIDIT_WEBHOOK_SECRET")
DIDIT_WORKFLOW_ID = os.getenv("DIDIT_WORKFLOW_ID")
DIDIT_CALLBACK_URL = os.getenv("DIDIT_CALLBACK_URL")

# Blockchain & smartcontract
BLOCKCHAIN_CONFIG = {
    "ENABLED": os.getenv("ENABLE_BLOCKCHAIN", "false").lower() == "true",
    "DEMO_MODE": os.getenv("BLOCKCHAIN_DEMO_MODE", "false").lower() == "true",
    "RPC_URL": os.getenv("BLOCKCHAIN_RPC_URL", "https://sepolia.base.org"),
    "PRIVATE_KEY": os.getenv("BLOCKCHAIN_PRIVATE_KEY"),
    "CHAIN_ID": int(os.getenv("BLOCKCHAIN_CHAIN_ID", "84532")),
    "CONTRACTS": {
        "userRegistry": os.getenv("CONTRACT_USER_REGISTRY"),
        "simSwapManager": os.getenv("CONTRACT_SIM_SWAP_MANAGER"),
        "accessControl": os.getenv("CONTRACT_ACCESS_CONTROL"),
    },
}


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['swap-backend-mj36.onrender.com', 'localhost', '127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "corsheaders",

    "customers.apps.CustomersConfig",
    "lines",
    "wallet",
    "swap",
    "vetting",
    "fraud",
    "audit",
    "blockchain",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
}

# Database

# tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': tmpPostgres.path.replace('/', ''),
#         'USER': tmpPostgres.username,
#         'PASSWORD': tmpPostgres.password,
#         'HOST': tmpPostgres.hostname,
#         'PORT': 5432,
#         'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
#     }
# }
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMP_VIDEO_DIR = os.path.join(BASE_DIR, 'tmp_videos')
if not os.path.exists(TEMP_VIDEO_DIR):
    os.makedirs(TEMP_VIDEO_DIR)
